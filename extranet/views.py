import datetime
import io
from monthdelta import monthdelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.db.models import Q, Sum, Count, F, Window, Value, FloatField
from django.db.models.functions import Coalesce, Replace
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import View, ListView
from django.views.generic.edit import FormView

from PyPDF2 import PdfFileWriter, PdfFileReader
import requests
from requests.auth import HTTPBasicAuth

from extranet import import_tasks
from extranet.forms import ExtranetClientSelectionForm, CustomAuthenticationForm
from extranet.models import IncomeQuality, Deliveries, Sales, SpeciesHarvest, Applied, CtaCte, TicketsAnalysis
from extranet.models import Notifications, ViewedNotifications
from extranet.tokens import account_activation_token

from website.utils import DownloadCSVBaseClass

from bh import settings


@login_required
@staff_member_required
def importdata(request, datatype):
    if datatype == 'ctacte':
        import_tasks.importCtaCteP()
    elif datatype == 'kilos':
        import_tasks.importKilos()
    elif datatype == 'applied':
        import_tasks.importApplied()
    elif datatype == 'analysis':
        import_tasks.importTicketsAnalysis()
    elif datatype == 'quality':
        import_tasks.importIncomeQuality()
    elif datatype == 'all':
        import_tasks.importCtaCteP()
        import_tasks.importKilos()
        import_tasks.importApplied()
        import_tasks.importTicketsAnalysis()
    else:
        raise Http404()

    return render(request, 'update_extranet.html')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        user = form.get_user()
        self.request.session['algoritmo_code'] = user.userinfo.algoritmo_code
        return HttpResponseRedirect(self.get_success_url())


class AccountActivationView(View):
    def get(self, request, *args, **kwargs):
        try:
            uidb64 = kwargs['uidb64']
            token = kwargs['token']
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        # Check token, mark account as active and confirm account
        if user is not None and account_activation_token.check_token(user, token):
            user.userinfo.account_confirmed = True
            user.userinfo.save()
            user.is_active = True
            user.save()
            # Set backend for user instead authenticate() function
            user.backend = 'django.contrib.auth.backends.AllowAllUsersModelBackend'
            login(request, user)
            request.session['algoritmo_code'] = user.userinfo.algoritmo_code

            return render(request, 'change_password.html', {'account_confirmed': True})
        else:
            return render(request, 'change_password.html', {'account_confirmed_error': True})


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = SetPasswordForm
    success_url = reverse_lazy('extranet')
    template_name = 'change_password.html'

    def form_valid(self, form):
        form.save()
        if self.request.user.userinfo.random_password == True:
            self.request.user.userinfo.random_password = False
            self.request.user.userinfo.save()
        if not self.request.user.userinfo.is_commercial:
            self.request.session['algoritmo_code'] = self.request.user.userinfo.algoritmo_code
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class ExtranetView(LoginRequiredMixin, FormView):
    template_name = 'extranet.html'
    form_class = ExtranetClientSelectionForm
    success_url = '/extranet/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        client = form.cleaned_data['client']
        self.request.session['algoritmo_code'] = client.algoritmo_code
        self.request.session['company_name'] = client.company_name
        return super(ExtranetView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = Notifications.objects.filter(active=True, date_to__gte=datetime.date.today())
        notifications_list = []
        notifications_id = []
        for n in notifications:
            if ViewedNotifications.objects.filter(notification=n.id, user=self.request.user).exists():
                pass
            else:
                notifications_list.append(n)
                notifications_id.append(n.id)
        context['notifications'] = notifications_list
        if len(notifications_id) > 0:
            self.request.session['notifications'] = notifications_id
        return context


class NotificationsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if 'notifications' in request.session:
            notifications = request.session['notifications']
            for n in notifications:
                not_obj = Notifications.objects.get(id=n)
                ViewedNotifications.objects.create(notification=not_obj, user=request.user, viewed=True)
            del request.session['notifications']
            return redirect(reverse('extranet'))
        else:
            return redirect('/')


class DateFilterBaseView(ListView):
    http_method_names = ['get',]
    allow_empty = True
    date_field = None
    since_date = None
    until_date = None
    initial = False
    date_format = '%Y-%m-%d'

    def get_since_date(self):
        since_date = self.since_date
        if since_date is None:
            try:
                since_date = self.kwargs['from']
            except KeyError:
                try:
                    since_date = self.request.GET['from']
                except KeyError:
                    return None
        format = self.date_format
        try:
            return datetime.datetime.strptime(since_date, format).date()
        except:
            return None

    def get_until_date(self):
        until_date = self.until_date
        if until_date is None:
            try:
                until_date = self.kwargs['to']
            except KeyError:
                try:
                    until_date = self.request.GET['to']
                except KeyError:
                    return None
        format = self.date_format
        try:
            return datetime.datetime.strptime(until_date, format).date()
        except:
            return None

    def get_context_data(self, **kwargs):
        context = {'from_date': self.get_since_date(),
                   'to_date': self.get_until_date(),
                   'initial': self.initial}
        context.update(kwargs)
        return super(DateFilterBaseView, self).get_context_data(**context)


class CtaCteView(LoginRequiredMixin, DateFilterBaseView):
    template_name = 'ctacte.html'

    def get(self, request, *args, **kwargs):
        ctacte_type = kwargs['ctacte_type']
        if ctacte_type != 'vencimiento' and ctacte_type != 'emision':
            raise Http404('Tipo de cuenta corriente iválido')
        if ctacte_type == 'emision':
            self.date_field = 'date_2'
        else:
            self.date_field = 'date_1'
        if self.get_since_date() is None and self.get_until_date() is None:
            self.since_date = (datetime.datetime.today() - monthdelta(1)).strftime(self.date_format)
            self.initial = True
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        ctacte_type = self.kwargs['ctacte_type']
        algoritmo_code = self.request.session['algoritmo_code']

        date_field = self.date_field
        since = self.get_since_date()
        until = self.get_until_date()
        initial_balance = {}
        if since:
            lookup_ib = {
                '%s__lt' % date_field: since
            }
            initial_balance = CtaCte.objects.filter(algoritmo_code=algoritmo_code).filter(**lookup_ib).aggregate(ib=Coalesce(Sum('amount_sign'),0))
        if until and since:
            lookup_kwargs = {
                '%s__gte' % date_field: since,
                '%s__lt' % date_field: until,
            }
        elif until:
            lookup_kwargs = {
                '%s__lt' % date_field: until,
            }
        else:
            lookup_kwargs = {
                '%s__gte' % date_field: since
            }
        queryset = CtaCte.objects\
            .filter(algoritmo_code=algoritmo_code)\
            .filter(**lookup_kwargs)\
            .annotate(ib=Value(initial_balance.get('ib', 0), output_field=FloatField()))\
            .annotate(row_balance=Window(Sum('amount_sign'), order_by=[F('%s' % date_field).asc(), F('voucher').asc(), F('amount_sign').asc()]) + F('initial_balance_countable') + F('ib'))\
            .values('date_1', 'date_2', 'voucher', 'concept', 'movement_type', 'amount_sign', 'initial_balance_countable', 'ib', 'row_balance').order_by('%s' % date_field, 'voucher', 'amount_sign')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ctacte_type'] = self.kwargs['ctacte_type']
        return context


class AppliedView(LoginRequiredMixin, DateFilterBaseView):
    template_name = 'applied.html'
    date_field = 'expiration_date'

    def get_queryset(self):
        algoritmo_code = self.request.session['algoritmo_code']

        date_field = self.date_field
        since = self.get_since_date()
        until = self.get_until_date()
        lookup_kwargs = {}
        initial_balance = {}
        if since:
            lookup_ib = {
                '%s__lt' % date_field: since
            }
            initial_balance = Applied.objects.filter(algoritmo_code=algoritmo_code).filter(**lookup_ib).aggregate(ib=Coalesce(Sum('amount_sign'),0))
        if until and since:
            lookup_kwargs = {
                '%s__gte' % date_field: since,
                '%s__lt' % date_field: until,
            }
        elif until:
            lookup_kwargs = {
                '%s__lt' % date_field: until,
            }
        elif since:
            lookup_kwargs = {
                '%s__gte' % date_field: since,
            }
        queryset = Applied.objects\
            .filter(algoritmo_code=algoritmo_code)\
            .filter(**lookup_kwargs)\
            .annotate(ib=Value(initial_balance.get('ib', 0), output_field=FloatField()))\
            .annotate(row_balance=Window(Sum('amount_sign'), order_by=[F('%s' % date_field).asc(), F('voucher').asc(), F('amount_sign').asc()]) + F('ib'))\
            .values('expiration_date', 'issue_date', 'voucher', 'concept', 'movement_type', 'amount_sign', 'ib', 'row_balance').order_by('%s' % date_field, 'voucher', 'amount_sign')
        return queryset


class HarvestFilterBaseView(ListView):
    current_species = None

    def set_current_species(self, checks):
        speciesharvest_filter = Q()
        for item in checks:
            speciesharvest_filter = speciesharvest_filter | Q(speciesharvest=item)
        self.current_species = speciesharvest_filter

    def get_species_for(self, algoritmo_code, movement_type):
        return SpeciesHarvest.objects\
            .filter(algoritmo_code=algoritmo_code, movement_type=movement_type)\
            .annotate(species_title=Replace('species_description', Value('COSECHA '), Value('')))\
            .values('species', 'harvest', 'speciesharvest', 'species_title', 'species_description')\
            .order_by('-harvest', 'speciesharvest')

    def get(self, request, *args, **kwargs):
        try:
            request.session['current_species'] = kwargs['checks']
            self.set_current_species(kwargs['checks'])
        except KeyError:
            try:
                request.session['current_species'] = request.GET.getlist('checks')
                self.set_current_species(request.GET.getlist('checks'))
            except KeyError:
                pass
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        algoritmo_code = self.request.session['algoritmo_code']
        current_species = self.current_species
        return context


class DeliveriesView(LoginRequiredMixin, HarvestFilterBaseView):
    template_name = 'deliveries.html'
    source_of_quality = settings.SOURCE_QUALITY_DATA

    def get_queryset(self):
        current_species = self.current_species
        if current_species:
            algoritmo_code = self.request.session['algoritmo_code']
            queryset = Deliveries.objects\
                .filter(algoritmo_code=algoritmo_code)\
                .filter(current_species)\
                .annotate(species_title=Replace('species_description', Value('COSECHA '), Value('')))\
                .values('date', 'voucher', 'gross_kg', 'humidity_percentage', 'humidity_kg', 'shaking_reduction', 'shaking_kg', 'volatile_reduction', 'volatile_kg', 'net_weight', 'factor', 'grade', 'number_1116A', 'external_voucher_number', 'driver_name', 'field_description', 'species_title')\
                .order_by('-harvest', 'species', 'field_description', 'date')
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        algoritmo_code = self.request.session['algoritmo_code']
        current_species = self.current_species
        context['species'] = self.get_species_for(algoritmo_code, 'D')
        if current_species:
            context['total'] = Deliveries.objects\
                .filter(algoritmo_code=algoritmo_code)\
                .filter(current_species)\
                .aggregate(Sum('net_weight'), Count('voucher'), Sum('humidity_kg'), Sum('shaking_kg'), Sum('volatile_kg'), Sum('gross_kg'))
            context['totals_by_field'] = list(
                Deliveries.objects\
                .filter(algoritmo_code=algoritmo_code)\
                .filter(current_species)\
                .annotate(species_title=Replace('species_description', Value('COSECHA '), Value('')))\
                .values('species_title', 'field_description')\
                .annotate(total_net=Sum('net_weight'), tickets_count=Count('voucher'), total_hum=Sum('humidity_kg'), total_sha=Sum('shaking_kg'), total_vol=Sum('volatile_kg'), total_gross=Sum('gross_kg'))\
                .order_by('-harvest', 'speciesharvest')
            )
            context['source_of_quality'] = self.source_of_quality
            if self.source_of_quality == 'ticket_analysis':
                # Use list() to evaluate QuerySet only once, otherwise queryset will be evaluated every time a ticket is searched
                context['quality'] = list(
                    TicketsAnalysis.objects\
                        .filter(algoritmo_code=algoritmo_code)\
                        .filter(current_species)\
                        .values('ticket', 'analysis_costs', 'gluten', 'analysis_item', 'percentage', 'bonus', 'reduction', 'item_descripcion')\
                        .order_by('item_descripcion')
                )
            elif self.source_of_quality == 'income_quality':
                context['quality'] = list(
                    IncomeQuality.objects\
                        .filter(algoritmo_code=algoritmo_code)\
                        .filter(current_species)\
                        .values('ticket', 'species', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5', 'item_6', 'item_7', 'item_8', 'item_9', 'item_10', 'item_11', 'item_12', 'item_13', 'item_14', 'item_15', 'bonus_item_1', 'bonus_item_2', 'bonus_item_3', 'bonus_item_4', 'bonus_item_5', 'bonus_item_6', 'bonus_item_7', 'bonus_item_8', 'bonus_item_9', 'bonus_item_10', 'bonus_item_11', 'bonus_item_12', 'bonus_item_13', 'bonus_item_14', 'bonus_item_15', 'reduction_item_1', 'reduction_item_2', 'reduction_item_3', 'reduction_item_4', 'reduction_item_5', 'reduction_item_6', 'reduction_item_7', 'reduction_item_8', 'reduction_item_9', 'reduction_item_10', 'reduction_item_11', 'reduction_item_12', 'reduction_item_13', 'reduction_item_14', 'reduction_item_15', 'gluten', 'humidity_percentage', 'humidity_volatile_reduction', 'humidity_volatile_kg', 'shaking_reduction', 'shaking_kg', 'volatile_percentage', 'volatile_kg', 'quality_percentage', 'quality_reduction')\
                        .order_by('ticket')
                )
        return context


class SalesView(LoginRequiredMixin, HarvestFilterBaseView):
    template_name = 'sales.html'

    def get_queryset(self):
        current_species = self.current_species
        if current_species:
            algoritmo_code = self.request.session['algoritmo_code']
            queryset = Sales.objects\
                .filter(algoritmo_code=algoritmo_code)\
                .filter(current_species)\
                .annotate(species_title=Replace('species_description', Value('COSECHA '), Value('')))\
                .values('id', 'date', 'voucher', 'field_description', 'service_billing_date', 'to_date', 'gross_kg', 'service_billing_number', 'number_1116A', 'price_per_yard', 'grade', 'driver_name', 'observations', 'species_description', 'indicator', 'species_title')\
                .order_by('-harvest', 'speciesharvest', 'indicator', 'date')
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        algoritmo_code = self.request.session['algoritmo_code']
        current_species = self.current_species
        context['species'] = self.get_species_for(algoritmo_code, 'S')
        if current_species:
            context['totals_by_sale'] = list(
                Sales.objects\
                .filter(algoritmo_code=algoritmo_code)\
                .filter(current_species)\
                .annotate(species_title=Replace('species_description', Value('COSECHA '), Value('')))\
                .values('species_title', 'indicator')\
                .annotate(total_gross=Sum('gross_kg'), total_pending=Sum('service_billing_number'), total_liquid=Sum('number_1116A'), total_count=Count('voucher'), total_in=Sum('gross_kg', filter=Q(gross_kg__gt=0)), total_out=Sum('gross_kg', filter=Q(gross_kg__lt=0)))\
                .order_by('-harvest', 'speciesharvest')
            )
            context['total_sales'] = Sales.objects.filter(algoritmo_code=algoritmo_code, indicator='2').filter(current_species).aggregate(Sum('net_weight'))
            context['total_to_set'] = Sales.objects.filter(algoritmo_code=algoritmo_code, indicator='2B').filter(current_species).aggregate(Sum('net_weight'))
            context['total_other'] = Sales.objects.filter(algoritmo_code=algoritmo_code, indicator='3').filter(current_species).aggregate(Sum('net_weight'))
            context['total_settled'] = Sales.objects.filter(algoritmo_code=algoritmo_code).filter(current_species).aggregate(Sum('number_1116A'))
        return context


class DownloadCtaCteCSVView(CtaCteView, DownloadCSVBaseClass):
    filename = 'Cuenta Corriente'
    headers = ('Fecha Vencimiento', 'Fecha Emisión', 'Comprobante', 'Concepto', 'Tipo de Movimiento', 'Importe', 'Saldo')
    template = 'csv_ctacte_template.txt'

    def get(self, request, *args, **kwargs):
        super(DownloadCtaCteCSVView, self).get(request, *args, **kwargs)
        response = self.get_csv_response()
        return response


class DownloadAppliedCSVView(AppliedView, DownloadCSVBaseClass):
    filename = 'Cuenta Corriente Aplicada'
    headers = ('Fecha Vencimiento', 'Fecha Emisión', 'Comprobante', 'Concepto', 'Tipo de Movimiento', 'Importe', 'Saldo')
    template = 'csv_applied_template.txt'

    def get(self, request, *args, **kwargs):
        super(DownloadAppliedCSVView, self).get(request, *args, **kwargs)
        response = self.get_csv_response()
        return response


class DownloadDeliveriesCSVView(DeliveriesView, DownloadCSVBaseClass):
    filename = 'Entregas'
    headers = ('Fecha', 'Comprobante', 'Kilos Brutos', '% Hum.', 'Kg. Hum.', '% Zarandeo', 'Kg. Zarandeo', '% Volatil', 'Kg. Volatil', 'Kilos Netos', 'Factor', 'Grado', 'Certificado', 'Número Externo', 'Chofer', 'Campo', 'Especie y Cosecha')
    template = 'csv_deliveries_template.txt'

    def get(self, request, *args, **kwargs):
        super(DownloadDeliveriesCSVView, self).get(request, *args, **kwargs)
        response = self.get_csv_response()
        return response


class DownloadSalesCSVView(SalesView, DownloadCSVBaseClass):
    filename = 'Ventas'
    headers = ('Fecha', 'Comprobante', 'Destino', 'Fecha Entrega Desde', 'Fecha Entrega Hasta', 'Kilos', 'Pend. TC', 'Liquidado', 'Precio por Quintal', 'Moneda', 'Observaciones', 'Especie y Cosecha')
    template = 'csv_sales_template.txt'

    def get(self, request, *args, **kwargs):
        super(DownloadSalesCSVView, self).get(request, *args, **kwargs)
        response = self.get_csv_response()
        return response


class DownloadPDFView(LoginRequiredMixin, View):
    vouchers = {
        'LC': {'codigo': ['C',], 'separator': ' ', 'url':''},
        'IC': {'codigo': ['C',], 'separator': ' ', 'url':''},
        'LB': {'codigo': ['B',], 'separator': ' ', 'url':''},
        'IB': {'codigo': ['B',], 'separator': ' ', 'url':''},
        'ND': {'codigo': ['HNDCER','HNDE','NDE','NDECAJ','NDECER','NDEPER',], 'separator': '_', 'url':'ventas/'},
        'NC': {'codigo': ['HNCCER','HNCR','NCR','NCRCER','NCRDEV','NCSCER',], 'separator': '_', 'url':'ventas/'},
        'FC': {'codigo': ['FAC','FACCER','FACD','FACSER','FASCER','HFAC','HFACER',], 'separator': '_', 'url':'ventas/'},
        'PC': {'codigo': ['PC',], 'separator': '_', 'url':'tesoreria/'},
        'OP': {'codigo': ['OP',], 'separator': '_', 'url':'tesoreria/'},
        'RE': {'codigo': ['RE',], 'separator': '_', 'url':'tesoreria/'},
        'VT': {'codigo': ['VT',], 'separator': '_', 'url':'cnv/'},
        'VF': {'codigo': ['VF',], 'separator': '_', 'url':'cnv/'},
    }

    def append_pdf(self, input, output):
        [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

    def merge_pdf(self, file1, file2):
        # Create instance por Write new PDF
        output = PdfFileWriter()
        pdf1 = PdfFileReader(io.BytesIO(file1))
        pdf2 = PdfFileReader(io.BytesIO(file2))
        self.append_pdf(pdf1,output)
        self.append_pdf(pdf2,output)
        # Init InMemory PDF file
        new_file = io.BytesIO()

        # Write PDF to buffer
        output.write(new_file)
        return new_file.getvalue()

    def search_file(self, voucher, voucher_date):
        voucher = voucher.split(' ')
        if self.vouchers.get(voucher[0], None) is None:
            return None
        else:
            separator = self.vouchers[voucher[0]]['separator']
            url = self.vouchers[voucher[0]]['url']
            for c in self.vouchers[voucher[0]]['codigo']:
                file_name = '{0}{1}{2}{3}{4}.pdf'.format(c, separator, voucher[1], separator, voucher[2])
                if 'tesoreria' in url:
                    file_url = 'http://{0}:{1}/{2}{3}/C{4}{5}{6}'.format(settings.RS_HOST, settings.RS_PORT, url, voucher_date, str(self.request.session['algoritmo_code']), separator, file_name)
                else:
                    file_url = 'http://{0}:{1}/{2}{3}'.format(settings.RS_HOST, settings.RS_PORT, url, file_name)
                r = requests.get(file_url, auth=HTTPBasicAuth(settings.RS_USER, settings.RS_PASS))
                if r.status_code == 200:
                    ##### FASCER Tickets Detail
                    if c == 'FASCER':
                        tickets_file_url = 'http://{0}:{1}/DETTK{2}{3}{4}{5}.pdf'.format(settings.RS_HOST, settings.RS_PORT, separator, voucher[1], separator, voucher[2])
                        rtk = requests.get(tickets_file_url, auth=HTTPBasicAuth(settings.RS_USER, settings.RS_PASS))
                        if rtk.status_code == 200:
                            r = self.merge_pdf(r.content, rtk.content)
                            return {'file':r, 'filename':file_name}
                    # If voucher is not FASCER or there is no DETTK then return the response content (file)
                    return {'file':r.content, 'filename':file_name}

    def get(self, request, *args, **kwargs):
        algoritmo_code = request.session['algoritmo_code']
        try:
            f = kwargs['f']
            d = kwargs['d']
        except KeyError:
            try:
                f = request.GET['f']
                d = request.GET['d']
            except KeyError:
                pass
        file = self.search_file(f, d)
        if file:
            response = HttpResponse(file['file'], content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file['filename'])
            return response
        else:
            raise Http404
