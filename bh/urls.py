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
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView

from website.views import IndexView, HistoricRainView, CareersView, DownloadRainView
from website.views import CurrencyView, BoardView, RainView
from extranet.views import CustomLoginView, AccountActivationView, ChangePasswordView, ExtranetView, NotificationsView
from extranet.views import CtaCteView, AppliedView, DeliveriesView, SalesView, DownloadCtaCteCSVView
from extranet.views import DownloadAppliedCSVView, DownloadDeliveriesCSVView, DownloadSalesCSVView, DownloadPDFView
from extranet.views import importdata
from extranet.forms import CustomAuthenticationForm

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('sentry-debug/', trigger_error),
    path('tinymce/', include('tinymce.urls')),

    path('admin/', admin.site.urls),

    path('', IndexView.as_view(), name='home'),
    path('empresa/', TemplateView.as_view(template_name='company.html'), name='company'),
    path('galeria/', TemplateView.as_view(template_name='gallery.html'), name='gallery'),
    path('contacto/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('lluvias-historico/', HistoricRainView.as_view(), name='historic_rain'),
    path('impuestos/', TemplateView.as_view(template_name='taxes.html'), name='taxes'),
    path('unidades-de-negocio/', TemplateView.as_view(template_name='units.html'), name='units'),
    path('trabaja-con-nosotros/', CareersView.as_view(), name='cv'),

    path('login/', CustomLoginView.as_view(template_name='login.html', authentication_form=CustomAuthenticationForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activar-cuenta/<slug:uidb64>/<slug:token>/', AccountActivationView.as_view(), name='activate_account'),
    path('cuenta/cambiar-password/', ChangePasswordView.as_view(), name='change_password'),
    path('cuenta/password-actualizada/', PasswordChangeDoneView.as_view(template_name='change_password_done.html'), name='password_change_done'),

    path('extranet/', ExtranetView.as_view(), name='extranet'),
    path('extranet/notificaciones/', NotificationsView.as_view(), name='notifications'),
    path('extranet/ctacte/pesos/<str:ctacte_type>/', CtaCteView.as_view(), name='ctacte'),
    path('extranet/ctacte/aplicada/', AppliedView.as_view(), name='applied'),
    path('extranet/entregas/', DeliveriesView.as_view(), name='deliveries'),
    path('extranet/ventas/', SalesView.as_view(), name='sales'),

    path('download/rain/', DownloadRainView.as_view(), name='download_rain'),
    path('download/pesos/<str:ctacte_type>/', DownloadCtaCteCSVView.as_view(), name='download_ctacte'),
    path('download/ctacte/aplicada/', DownloadAppliedCSVView.as_view(), name='download_applied'),
    path('download/entregas/', DownloadDeliveriesCSVView.as_view(), name='download_deliveries'),
    path('download/ventas/', DownloadSalesCSVView.as_view(), name='download_sales'),
    path('download/', DownloadPDFView.as_view(), name='download_pdf'),

    path('monedas/', CurrencyView.as_view(), name='currency'),
    path('pizarras/', BoardView.as_view(), name='board'),
    path('lluvias/', RainView.as_view(), name='rain'),

    path('importar/<str:datatype>/', importdata, name='import_data'),

    # path('400/', views.handler404, name='handler400'),
    # path('404/', views.handler404, name='handler404'),
    # path('500/', views.handler500, name='handler500'),

    # Internazionalization
    path('i18n/', include('django.conf.urls.i18n')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = 'website.views.handler404'
handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'
