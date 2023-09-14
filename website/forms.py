from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from tinymce.widgets import TinyMCE

from website.models import Careers
from extranet.models import UserInfo, Notifications


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _('¡Ops! parece que su usuario y contraseña no son validos. Inténtelo nuevamente.'),
        'inactive': _('Su cuenta aún no ha sido activada. Ingrese al link de activación que recibió por correo.'),
    }


class ExtranetClientSelectionForm(forms.Form):
    client = forms.ModelChoiceField(queryset=UserInfo.objects.all().order_by('company_name'), required=True, empty_label='- - - - - -')


class UserCreationForm(ModelForm):
    username = forms.CharField(required=True, label='Nombre de usuario')
    email = forms.EmailField(required=True, label='Direccion de email')

    class Meta:
        model = User
        fields = ('username', 'email',)


class NotificationCreationForm(ModelForm):

    class Meta:
        model = Notifications
        fields = ('title', 'notification', 'active', 'date_from', 'date_to',)
        widgets = {
            'notification': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }


class CareerCreationForm(ModelForm):

    class Meta:
        model = Careers
        fields = ('title', 'active', 'description', 'requirements',)
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'requirements': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }


class DateInput(forms.DateInput):
    input_type = 'date'
