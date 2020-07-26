from django.shortcuts import render

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


def index(request):
    currency = Currencies.objects.order_by('-date')[:1]
    board = Board.objects.order_by('-date')[:1]
    rain = Rain.objects.order_by('-date')[:1]
    rain = RainDetail.objects.filter(rain=rain).order_by('city__city')

    return render(request, 'index.html', {'currency': currency, 'board': board, 'rain': rain})
