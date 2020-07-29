import datetime 
from collections import OrderedDict
import json

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.views.defaults import page_not_found, server_error
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear
from django.core import serializers

from website.models import CtaCte
from website.models import Deliveries
from website.models import Sales
from website.models import SpeciesHarvest
from website.models import Applied
from website.models import UserInfo
from website.models import Notifications
from website.models import ViewedNotifications
from website.models import Currencies
from website.models import Board
from website.models import TicketsAnalysis
from website.models import City
from website.models import Rain
from website.models import RainDetail

from website.forms import ExtranetClientSelectionForm


# def cp(request):
#     pass
# def downloadRainExcel(request):
#     pass


def handler404(request, exception):
    return page_not_found(request, exception, template_name='404.html')


def handler500(request):
    return server_error(request, template_name='500.html')


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currency'] = Currencies.objects.order_by('-date')[:1]
        context['board'] = Board.objects.order_by('-date')[:1]
        rain = Rain.objects.order_by('-date')[:1]
        context['rain'] = RainDetail.objects.filter(rain=rain).order_by('city__city')
        return context


class CurrencyView(ListView):
    http_method_names = ['post',]
    model = Currencies

    def post(self, request, *args, **kwargs):
        data = None
        get_date = request.POST.get('cDate')
        currency = Currencies.objects.filter(date=get_date)
        if currency:
            data = serializers.serialize('json',currency)
        return JsonResponse({'data': data})


class BoardView(ListView):
    http_method_names = ['post',]
    model = Board

    def post(self, request, *args, **kwargs):
        data = None
        get_date = request.POST.get('bDate')
        board = Board.objects.filter(date=get_date)
        if board:
            data = serializers.serialize('json',board)
        return JsonResponse({'data': data})


class RainView(ListView):
    http_method_names = ['post',]
    model = RainDetail

    def post(self, request, *args, **kwargs):
        data = None
        get_date = request.POST.get('rDate')
        rain = RainDetail.objects.filter(rain=get_date).values('rain', 'city__city', 'mm').order_by('city__city')
        if rain:
            rain_data = []
            for r in rain:
                temp = {}
                temp['date'] = str(r['rain'])
                temp['city'] = r['city__city']
                temp['mm'] = r['mm']
                rain_data.append(temp)
            data = json.dumps(rain_data)
            print(data)
        return JsonResponse({'data': data})


class HistoricRainView(TemplateView):
    template_name = 'historic_rain.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        # Filter City = 1 only por Arrecifes
        rain = RainDetail.objects.filter(city=1).annotate(month=ExtractMonth('rain'), year=ExtractYear('rain')).values('month', 'year').annotate(mmsum=Sum('mm')).order_by('-year', 'month')
        print(rain)
        history = OrderedDict()
        month_avg = OrderedDict()
        prev_year = 0
        prev_month = 0

        for r in rain:
            # year = datetime.datetime.strptime(r['year'], "%Y-%m-%d").date().year
            # month = datetime.datetime.strptime(r['month'], "%Y-%m-%d").date().month
            year = r['year']
            month = r['month']
            if history.get(year, None) is None:
                history[year] = OrderedDict()
                history[year]['rain'] = OrderedDict()
                history[year]['total'] = 0
            if month_avg.get(month, None) is None:
                month_avg[month] = OrderedDict()
                month_avg[month]['sum'] = 0
                month_avg[month]['count'] = 0
            if year == prev_year or prev_year == 0:
                if prev_month + 1 == month or prev_month == 0:
                    # history[year]['rain'][month] = r['mmsum']
                    history[year]['rain'][month] = OrderedDict()
                    history[year]['rain'][month]['name'] = months[month-1]
                    history[year]['rain'][month]['mm'] = r['mmsum']
                    history[year]['total'] += r['mmsum']
                    month_avg[month]['sum'] += r['mmsum']
                    month_avg[month]['count'] += 1
                else:
                    for i in range(prev_month+1, month):
                        # history[year]['rain'][datetime.datetime(year,i,1).date().month] = 0
                        history[year]['rain'][datetime.datetime(year,i,1).date().month] = OrderedDict()
                        history[year]['rain'][datetime.datetime(year,i,1).date().month]['name'] = months[datetime.datetime(year,i,1).date().month - 1]
                        history[year]['rain'][datetime.datetime(year,i,1).date().month]['mm'] = 0
                        if month_avg.get(datetime.datetime(year,i,1).date().month, None) is None:
                            month_avg[datetime.datetime(year,i,1).date().month] = OrderedDict()
                            month_avg[datetime.datetime(year,i,1).date().month]['sum'] = 0
                            month_avg[datetime.datetime(year,i,1).date().month]['count'] = 0
                        month_avg[datetime.datetime(year,i,1).date().month]['count'] += 1
                    # history[year]['rain'][month] = r['mmsum']
                    history[year]['rain'][month] = OrderedDict()
                    history[year]['rain'][month]['name'] = months[month-1]
                    history[year]['rain'][month]['mm'] = r['mmsum']
                    history[year]['total'] += r['mmsum']
                    month_avg[month]['sum'] += r['mmsum']
                    month_avg[month]['count'] += 1
            else:
                # history[year]['rain'][month] = r['mmsum']
                history[year]['rain'][month] = OrderedDict()
                history[year]['rain'][month]['name'] = months[month-1]
                history[year]['rain'][month]['mm'] = r['mmsum']
                history[year]['total'] += r['mmsum']
                month_avg[month]['sum'] += r['mmsum']
                month_avg[month]['count'] += 1

            prev_year = year
            prev_month = month
        
        context['history'] = history
        context['month_avg'] = month_avg
        context['months'] = months
        return context


class ExtranetView(LoginRequiredMixin, FormView):
    template_name = 'extranet.html'
    form_class = ExtranetClientSelectionForm
    success_url = '/extranet/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        client = form.cleaned_data['client']
        client_selected = UserInfo.objects.filter(algoritmo_code=client).values('algoritmo_code', 'company_name')
        for d in client_selected:
            request.session['algoritmo_code'] = d['algoritmo_code']
            request.session['company_name'] = d['company_name']
        return super().form_valid(form)
    
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
            request.session['notifications'] = notifications_id
        clients = User.objects.filter(is_staff=False, userinfo__is_commercial=False).values('userinfo__algoritmo_code', 'userinfo__company_name').order_by('userinfo__company_name')
        context['clients'] = clients        
        return context