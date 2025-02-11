import json

from itertools import groupby
from operator import itemgetter

from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.defaults import page_not_found, server_error
from django.http import JsonResponse

from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.core import serializers

from website.models import Currencies
from website.models import Board
from website.models import Rain
from website.models import RainDetail
from website.models import Careers

from website.utils import DownloadCSVBaseClass




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


class CareersView(TemplateView):
    template_name = 'cv.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['careers'] = Careers.objects.filter(active=True)
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
        return JsonResponse({'data': data})


class HistoricRainView(TemplateView):
    template_name = 'historic_rain.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['months'] = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        # Filter City = 1 only por Arrecifes
        rain = RainDetail.objects.filter(city=1).annotate(month=ExtractMonth('rain'), year=ExtractYear('rain')).values('month', 'year').annotate(mmsum=Sum('mm')).order_by('-year', 'month')
        all_months = list(range(1, 13))
        grouped_rain_by_year = []
        for key, group in groupby(rain, key=itemgetter('year')):
            months = list(group)
            existing_months = {month['month']: month for month in months}
            complete_months = [{'month': m, 'year': key, 'mmsum': existing_months.get(m, {'mmsum': 0})['mmsum']} for m in all_months]
            grouped_rain_by_year.append({'year': key, 'month': complete_months})
        context['rain'] = grouped_rain_by_year
        return context


class DownloadRainView(DownloadCSVBaseClass):
    filename = 'Historico Lluvias'
    headers = ('Mes', 'Año', 'Milimetros')
    template = 'csv_rain_template.txt'

    def get_queryset(self):
        queryset = RainDetail.objects.filter(city=1).annotate(month=ExtractMonth('rain'), year=ExtractYear('rain')).values('month', 'year').annotate(mmsum=Sum('mm')).order_by('-year', 'month')
        return queryset

    def get(self, request, *args, **kwargs):
        response = self.get_csv_response()
        return response