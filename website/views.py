from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.defaults import page_not_found, server_error
from django.http import JsonResponse

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
        if request.is_ajax():
            get_date = request.POST.get('cDate')
            currency = Currencies.objects.filter(date=get_date)
            if curency:
                data = serializers.serialize('json',currency)
        return JsonResponse({'data': data})


class BoardView(ListView):
    http_method_names = ['post',]
    model = Board

    def post(self, request, *args, **kwargs):
        data = None
        if request.is_ajax():
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
        if request.is_ajax():
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


# def extranet(request):
#     pass
# def auth_logout(request):
#     pass
# def historic_rain(request):
#     pass
# def cp(request):
#     pass