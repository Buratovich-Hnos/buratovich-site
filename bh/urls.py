"""bh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView, LoginView

from website import views
from website.forms import CustomAuthenticationForm

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.IndexView.as_view(), name='home'),
    path('empresa/', TemplateView.as_view(template_name='company.html'), name='company'),
    path('galeria/', TemplateView.as_view(template_name='gallery.html'), name='gallery'),
    path('contacto/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('lluvias-historico/', views.HistoricRainView.as_view(), name='historic_rain'),
    path('impuestos/', TemplateView.as_view(template_name='taxes.html'), name='taxes'),
    path('unidades-de-negocio/', TemplateView.as_view(template_name='units.html'), name='units'),
    path('trabaja-con-nosotros/', TemplateView.as_view(template_name='cv.html'), name='cv'),
    # path('cp/', views.cp, name='cp'),

    path('login/', LoginView.as_view(template_name='login.html', authentication_form=CustomAuthenticationForm), name='login'),
    # path('login/invalido/', views.auth_login_invalid, name='login_invalid'),
    # path('login/requerido/', views.auth_login_required, name='login_required'),
    # path('login/cuenta-inactiva/', views.auth_login_inactive_account, name='login_inactive_account'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('activar-cuenta/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.auth_activate_account, name='activate_account'),
    # path('cuenta/cambiar-password/', views.change_password, name='change_password'),

    path('extranet/', views.ExtranetView.as_view(), name='extranet'),
    # path('extranet/notificaciones/', views.notifications, name='notifications'),
    # path('extranet/ctacte/pesos/<str:ctacte_type>/', views.ctacte, name='ctacte'),
    # path('extranet/ctacte/aplicada/', views.applied, name='applied'),
    # path('extranet/entregas/', views.deliveries, name='deliveries'),
    # path('extranet/ventas/', views.sales, name='sales'),

    # path('downloadexcel/rain/', views.downloadRainExcel, name='download_rain'),
    # path('downloadexcel/(?P<module>[0-9A-Za-z_\-]+)/', views.downloadexcel, name='downloadexcel'),
    # path('downloadexcel/(?P<module>[0-9A-Za-z_\-]+)(?:/(?P<type_module>[0-9A-Za-z_\-]+))/', views.downloadexcel, name='downloadexcel'),
    # path('download/', views.downloadPDFExtranet, name='downloadPDF'),

    path('monedas/', views.CurrencyView.as_view(), name='currency'),
    path('pizarras/', views.BoardView.as_view(), name='board'),
    path('lluvias/', views.RainView.as_view(), name='rain'),

    # path('importar/<str:datatype>/', views.importdata, name='importdata'),

    # path('400/', views.handler404, name='handler400'),
    # path('404/', views.handler404, name='handler404'),
    # path('500/', views.handler500, name='handler500'),

    # Internazionalization
    path('i18n/', include('django.conf.urls.i18n')),
]

handler400 = 'website.views.handler404'
handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'