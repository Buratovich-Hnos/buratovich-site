from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from tinymce.widgets import TinyMCE

from website.models import Careers


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
