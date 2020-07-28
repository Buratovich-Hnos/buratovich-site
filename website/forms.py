from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _('Su cuenta aún no ha sido activada. Ingrese al link de activación que recibió por correo.'),
                code='inactive',
            )


class ExtranetClientSelectionForm(forms.Form):
    client = forms.ChoiceField(required=True)