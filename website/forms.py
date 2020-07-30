from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext, gettext_lazy as _

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _('¡Ops! parece que su usuario y contraseña no son validos. Inténtelo nuevamente.'),
        'inactive': _('Su cuenta aún no ha sido activada. Ingrese al link de activación que recibió por correo.'),
    }


class ExtranetClientSelectionForm(forms.Form):
    client = forms.ChoiceField(required=True)