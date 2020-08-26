from datetime import datetime
from django.core import validators

from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _

from tinymce.widgets import TinyMCE

from website.models import UserInfo, Notifications


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _('¡Ops! parece que su usuario y contraseña no son validos. Inténtelo nuevamente.'),
        'inactive': _('Su cuenta aún no ha sido activada. Ingrese al link de activación que recibió por correo.'),
    }


class ExtranetClientSelectionForm(forms.Form):
    client = forms.ModelChoiceField(queryset=UserInfo.objects.all(), required=True, empty_label='- - - - - -')


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


class DateInput(forms.DateInput):
    input_type = 'date'

class CP(forms.Form):

    harvest_list = (('0000', '------'),)
    date = datetime.now().year
    for year in range(date-3,date+1):
        harvest_list += ((str(year)[-2:] + str(year+1)[-2:], str(year)[-2:] + '/' + str(year+1)[-2:]),)

    SPECIES = (
            ('0000', '------'),
            ('ALGO', 'Algodón'),
            ('AVEN', 'Avena'),
            ('CART', 'Cártamo'),
            ('CEBA', 'Cebada'),
            ('CECE', 'Cebada Cervecera'),
            ('COLZ', 'Colza'),
            ('COL0', 'Colza Doble 00'),
            ('CUAR', 'Cuarta de Cebada'),
            ('GIRA', 'Girasol'),
            ('LINO', 'Lino'),
            ('MAIZ', 'Maíz'),
            ('MAMA', 'Maíz Mav'),
            ('MAPI', 'Maíz Pisingallo'),
            ('MANI', 'Maní'),
            ('SOJA', 'Soja'),
            ('SORG', 'Sorgo'),
            ('TRIG', 'Trigo'),
            ('TRIC', 'Trigo Candeal'),
            ('TRIP', 'Trigo Pan'),
    )

    QUALITY = (
        ('DECLARACION', 'Declaración de Calidad'),
        ('CONFORME', 'Conforme'),
        ('CONDICIONAL', 'Condicional'),
    )

    numeric = validators.RegexValidator(r'^[0-9]*$', 'Solo se permiten numeros.')
    rate_max_value = validators.MaxValueValidator(999.9999)

    cp = forms.FileField(label='Carta de Porte')
    ownership_line = forms.BooleanField(label='Titular Carta de Porte', required=False)
    load_date = forms.DateField(label='Fecha de Carga', widget=DateInput)
    ctg = forms.CharField(label='CTG', max_length=8, strip=True, validators=[numeric], required=False)
    renspa = forms.CharField(label='RENSPA', max_length=20, strip=True, validators=[numeric], required=False)
    intermediary = forms.CharField(label='Intermediario', max_length=45, strip=True, required=False)
    intermediary_cuit = forms.CharField(label='CUIT', max_length=11, strip=True, validators=[numeric], required=False)
    sender = forms.CharField(label='Remitente Comercial', max_length=45, strip=True, required=False)
    sender_cuit = forms.CharField(label='CUIT', max_length=11, strip=True, validators=[numeric], required=False)
    broker = forms.CharField(label='Corredor Comprador', max_length=45, strip=True, required=False)
    broker_cuit = forms.CharField(label='CUIT', max_length=11, strip=True, validators=[numeric], required=False)
    mat = forms.CharField(label='Mercado a Término', max_length=45, strip=True, required=False)
    mat_cuit = forms.CharField(label='CUIT', max_length=11, strip=True, validators=[numeric], required=False)
    broker_seller = forms.CharField(label='Corredor Vendedor', max_length=45, strip=True, required=False)
    broker_seller_cuit = forms.CharField(label='CUIT', max_length=11, strip=True, validators=[numeric], required=False)
    representative = forms.CharField(label='Entregador', max_length=45, strip=True, required=False)
    representative_cuit = forms.CharField(label='CUIT', max_length=11, validators=[numeric], strip=True, required=False)
    addressee = forms.CharField(label='Destinatario', max_length=45, strip=True)
    addressee_cuit = forms.CharField(label='CUIT', max_length=11, validators=[numeric], strip=True)
    destination = forms.CharField(label='Destino', max_length=45, strip=True)
    destination_cuit = forms.CharField(label='CUIT', max_length=11, validators=[numeric], strip=True)
    freight_broker = forms.CharField(label='Intermediario del Flete', max_length=45, strip=True)
    freight_broker_cuit = forms.CharField(label='CUIT', max_length=11, validators=[numeric], strip=True)
    carrier = forms.CharField(label='Transportista', max_length=45, strip=True)
    carrier_cuit = forms.CharField(label='CUIT', max_length=11, validators=[numeric], strip=True)
    driver = forms.CharField(label='Chofer', max_length=45, strip=True)
    driver_cuit = forms.CharField(label='CUIT/CUIL', max_length=11, validators=[numeric], strip=True)
    harvest = forms.ChoiceField(label='Cosecha', choices=harvest_list)
    species = forms.ChoiceField(label='Grano/Especie', choices=SPECIES)
    species_type = forms.CharField(label='Tipo', max_length=18, strip=True, required=False)
    contract = forms.CharField(label='Contrato Nro.', max_length=17, strip=True, required=False)
    destination_load = forms.BooleanField(label='La carga será pesada en destino', required=False)
    estimated_kg = forms.IntegerField(label='Kilos Estimados', max_value=999999 , required=False)
    quality = forms.ChoiceField(label='Calidad', choices=QUALITY, widget=forms.RadioSelect)
    gross_kg = forms.IntegerField(label='Peso Bruto (Kgrs.)', max_value=999999 , required=False)
    tare_kg = forms.IntegerField(label='Peso Tara (Kgrs.)', max_value=999999 , required=False)
    net_kg = forms.IntegerField(label='Peso Neto (Kgrs.)', max_value=999999 , required=False)
    observations = forms.CharField(label='Observaciones', widget=forms.Textarea, required=False)
    stablishment = forms.CharField(label='Establecimiento', max_length=23, strip=True)
    address = forms.CharField(label='Dirección', max_length=45, strip=True)
    city = forms.CharField(label='Localidad', max_length=23, strip=True)
    state = forms.CharField(label='Provincia', max_length=23, strip=True)
    destination_address = forms.CharField(label='Dirección', max_length=45, strip=True)
    destination_city = forms.CharField(label='Localidad', max_length=23, strip=True)
    destination_state = forms.CharField(label='Provincia', max_length=23, strip=True)
    freight_payer = forms.CharField(label='Pagador del Flete', max_length=39, strip=True, required=False)
    truck = forms.CharField(label='Patente Camión', max_length=7, strip=True)
    trailer = forms.CharField(label='Patente Acoplado', max_length=7, strip=True)
    km = forms.IntegerField(label='Km a recorrer', max_value=9999 , required=False)
    ref_rate = forms.FloatField(label='Tarifa de Referencia', max_value=9999.9999, validators=[rate_max_value])
    rate = forms.FloatField(label='Tarifa', max_value=9999.9999, validators=[rate_max_value])
    fumigant_dni = forms.CharField(label='DNI', max_length=10, strip=True, validators=[numeric], required=False)
    fumigant_observation = forms.CharField(label='Aclaración', max_length=50, strip=True, required=False)

    def clean_cp(self):
        content = self.cleaned_data['cp']
        content_type = content.content_type
        if content_type in settings.CP_CONTENT_TYPES:
            if content.size > settings.CP_MAX_UPLOAD_SIZE:
                raise forms.ValidationError('El archivo es demasiado grande. El limite es %s, y el archivo subido pesa %s.' % (filesizeformat(settings.CP_MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        else:
            raise forms.ValidationError('Solo se permiten subir archivos PDF.')
        return content
