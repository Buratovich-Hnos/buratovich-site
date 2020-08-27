from django.db import models
from django.contrib.auth.models import User


# User related info
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    algoritmo_code = models.IntegerField(unique=True, verbose_name='Cuenta Algoritmo')
    company_name = models.CharField(max_length=150, verbose_name='Razón Social')
    is_commercial = models.BooleanField(default=False, verbose_name='Es Comercial?')
    account_confirmed = models.BooleanField(default=False, verbose_name='Cuenta Confirmada?')
    random_password = models.BooleanField(default=True, verbose_name='Password Aleatorio')

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class TicketsAnalysis(models.Model):
    algoritmo_code = models.IntegerField(verbose_name='Cuenta Algoritmo')
    ticket = models.CharField(max_length=16, verbose_name='Ticket')
    field = models.IntegerField(verbose_name='Campo')
    field_description = models.CharField(max_length=100, verbose_name='Nombre de Campo')
    species = models.CharField(max_length=4, verbose_name='Especie')
    harvest = models.CharField(max_length=4, verbose_name='Cosecha')
    speciesharvest = models.CharField(max_length=8, verbose_name='Especie Cosecha', null=True)
    grade = models.IntegerField(verbose_name='Grado')
    factor = models.FloatField(verbose_name='Factor')
    analysis_costs = models.FloatField(verbose_name='Gastos de Analisis')
    gluten = models.IntegerField(verbose_name='Gluten')
    analysis_item = models.IntegerField(verbose_name='Rubro de Analisis')
    percentage = models.FloatField(verbose_name='Porcentaje')
    bonus = models.FloatField(verbose_name='Bonificacion')
    reduction = models.FloatField(verbose_name='Rebaja')
    item_descripcion = models.CharField(max_length=100, verbose_name='Descripcion')

    def __str__(self):
        return self.ticket
    class Meta:
        verbose_name = 'Analisis por Ticket'


class Deliveries(models.Model):
    algoritmo_code = models.IntegerField(verbose_name='Cuenta Algoritmo')
    name = models.CharField(max_length=150, verbose_name='Razón Social')
    indicator = models.CharField(max_length=1, verbose_name='Indicador')
    species = models.CharField(max_length=4, verbose_name='Especie')
    harvest = models.CharField(max_length=4, verbose_name='Cosecha')
    speciesharvest = models.CharField(max_length=8, verbose_name='Especie Cosecha', null=True)
    species_description = models.CharField(max_length=50, verbose_name='Especie y Cosecha')
    field = models.IntegerField(verbose_name='Codigo de Campo')
    field_description = models.CharField(max_length=100, verbose_name='Nombre de Campo')
    date = models.DateField(null=True, verbose_name='Fecha')
    voucher = models.CharField(max_length=16, verbose_name='Comprobante')
    gross_kg = models.IntegerField(verbose_name='Peso Bruto')
    humidity_percentage = models.FloatField(verbose_name='Humedad (%)')
    humidity_reduction = models.FloatField(verbose_name='Merma de Humedad')
    humidity_kg = models.IntegerField(verbose_name='Kilos de Humedad')
    shaking_reduction = models.FloatField(verbose_name='Merma de Zarandeo')
    shaking_kg = models.IntegerField(verbose_name='Kilos de Zarandeo')
    volatile_reduction = models.FloatField(verbose_name='Merma Volatil')
    volatile_kg = models.IntegerField(verbose_name='Kilos Volatil')
    price_per_yard = models.FloatField(verbose_name='Precio por Quintal')
    driver_code = models.IntegerField(verbose_name='Chofer')
    driver_name = models.CharField(max_length=150, verbose_name='Nombre del Chofer')
    factor = models.FloatField(verbose_name='Factor')
    grade = models.IntegerField(verbose_name='Grado')
    gluten = models.IntegerField(verbose_name='Gluten')
    number_1116A = models.IntegerField(verbose_name='Numero 1116A')
    km = models.IntegerField(verbose_name='Kilometros')
    external_voucher_number = models.IntegerField(verbose_name='Numero Comprobante Externo')
    service_billing_number = models.IntegerField(verbose_name='Numero Factura de Servicios')
    service_billing_date = models.DateField(null=True, verbose_name='Fecha Factura de Servicios')
    service_billing = models.CharField(max_length=50, verbose_name='Factura de Servicios')
    to_date = models.DateField(null=True, verbose_name='Fecha Entrega Hasta')
    observations = models.CharField(max_length=300, verbose_name='Observaciones')
    follow_destination = models.CharField(max_length=2, verbose_name='Sigue a Destino')
    net_weight = models.IntegerField(verbose_name='Peso Neto')
    tare = models.IntegerField(verbose_name='Tara')

    def __str__(self):
        return self.voucher
    class Meta:
        verbose_name = 'Entregas'


class Sales(models.Model):
    algoritmo_code = models.IntegerField(verbose_name='Cuenta Algoritmo')
    name = models.CharField(max_length=150, verbose_name='Razón Social')
    indicator = models.CharField(max_length=1, verbose_name='Indicador')
    species = models.CharField(max_length=4, verbose_name='Especie')
    harvest = models.CharField(max_length=4, verbose_name='Cosecha')
    speciesharvest = models.CharField(max_length=8, verbose_name='Especie Cosecha', null=True)
    species_description = models.CharField(max_length=50, verbose_name='Especie y Cosecha')
    field = models.IntegerField(verbose_name='Codigo de Campo')
    field_description = models.CharField(max_length=100, verbose_name='Nombre de Campo')
    date = models.DateField(null=True, verbose_name='Fecha')
    voucher = models.CharField(max_length=16, verbose_name='Comprobante')
    gross_kg = models.IntegerField(verbose_name='Peso Bruto')
    humidity_percentage = models.FloatField(verbose_name='Humedad (%)')
    humidity_reduction = models.FloatField(verbose_name='Merma de Humedad')
    humidity_kg = models.IntegerField(verbose_name='Kilos de Humedad')
    shaking_reduction = models.FloatField(verbose_name='Merma de Zarandeo')
    shaking_kg = models.IntegerField(verbose_name='Kilos de Zarandeo')
    volatile_reduction = models.FloatField(verbose_name='Merma Volatil')
    volatile_kg = models.IntegerField(verbose_name='Kilos Volatil')
    price_per_yard = models.FloatField(verbose_name='Precio por Quintal')
    driver_code = models.IntegerField(verbose_name='Chofer')
    driver_name = models.CharField(max_length=150, verbose_name='Nombre del Chofer')
    factor = models.FloatField(verbose_name='Factor')
    grade = models.IntegerField(verbose_name='Grado')
    gluten = models.IntegerField(verbose_name='Gluten')
    number_1116A = models.IntegerField(verbose_name='Numero 1116A')
    km = models.IntegerField(verbose_name='Kilometros')
    external_voucher_number = models.IntegerField(verbose_name='Numero Comprobante Externo')
    service_billing_number = models.IntegerField(verbose_name='Numero Factura de Servicios')
    service_billing_date = models.DateField(null=True, verbose_name='Fecha Factura de Servicios')
    service_billing = models.CharField(max_length=50, verbose_name='Factura de Servicios')
    to_date = models.DateField(null=True, verbose_name='Fecha Entrega Hasta')
    observations = models.CharField(max_length=300, verbose_name='Observaciones')
    follow_destination = models.CharField(max_length=2, verbose_name='Sigue a Destino')
    net_weight = models.IntegerField(verbose_name='Peso Neto')
    tare = models.IntegerField(verbose_name='Tara')

    def __str__(self):
        return self.voucher

    class Meta:
        verbose_name = 'Ventas'


class SpeciesHarvest(models.Model):
    algoritmo_code = models.IntegerField(verbose_name='Cuenta Algoritmo')
    movement_type = models.CharField(max_length=1, verbose_name='Tipo Movimiento')
    species = models.CharField(max_length=4, verbose_name='Especie')
    harvest = models.CharField(max_length=4, verbose_name='Cosecha')
    speciesharvest = models.CharField(max_length=8, verbose_name='Especie Cosecha', null=True)
    species_description = models.CharField(max_length=50, verbose_name='Especie y Cosecha')

    def __str__(self):
        return self.species_description

    class Meta:
        verbose_name = 'Especies y Cosechas'


class Applied(models.Model):
    algoritmo_code = models.IntegerField(verbose_name='Cuenta Algoritmo')
    name = models.CharField(max_length=150, verbose_name='Razón Social')
    movement_type = models.CharField(max_length=7, verbose_name='Tipo Movimiento')
    voucher = models.CharField(max_length=16, verbose_name='Comprobante')
    voucher_date = models.DateField(null=True, verbose_name='Fecha Comprobante')
    expiration_date = models.DateField(null=True, verbose_name='Fecha Vencimiento')
    issue_date = models.DateField(null=True, verbose_name='Fecha Emision')
    concept = models.CharField(max_length=200, verbose_name='Concepto')
    cta_cte = models.CharField(max_length=1, verbose_name='Codigo de Cta. Cte.')
    cta_cte_description = models.CharField(max_length=50, verbose_name='Descripcion de Cta. Cte.')
    currency = models.CharField(max_length=1, verbose_name='Moneda')
    amount_sign = models.FloatField(verbose_name='Importe Signo')
    exchange_rate = models.FloatField(verbose_name='Tipo de Cambio Emisión')

    def __str__(self):
        return self.voucher

    class Meta:
        verbose_name = 'Cuenta Corriente Aplicada'
        verbose_name_plural = 'Cuentas Corrientes Aplicadas'


class CtaCte(models.Model):
    algoritmo_code = models.IntegerField(verbose_name='Cuenta Algoritmo')
    name = models.CharField(max_length=150, verbose_name='Razón Social')
    initial_balance_countable = models.FloatField(verbose_name='Saldo Inicial Contable')
    balance = models.FloatField(verbose_name='Saldo')
    voucher = models.CharField(max_length=16, verbose_name='Comprobante')
    voucher_date = models.DateField(null=True, verbose_name='Fecha Comprobante')
    concept = models.CharField(max_length=200, verbose_name='Concepto')
    currency = models.CharField(max_length=1, verbose_name='Moneda')
    movement_type = models.CharField(max_length=7, verbose_name='Tipo Movimiento')
    exchange_rate = models.FloatField(verbose_name='Tipo de Cambio Emisión')
    date_1 = models.DateField(null=True, verbose_name='Fecha Vencimiento')
    date_2 = models.DateField(null=True, verbose_name='Fecha Emisión')
    amount_sign = models.FloatField(verbose_name='Importe Signo')
    cta_cte = models.CharField(max_length=1, verbose_name='Tipo Cta. Cte.')
    cta_cte_name = models.CharField(max_length=80, verbose_name='Descripcion Cta. Cte.')

    def __str__(self):
        return self.voucher

    class Meta:
        verbose_name = 'Cuenta Corriente'
        verbose_name_plural = 'Cuentas Corrientes'


class Currencies(models.Model):
    date = models.DateField(verbose_name='Fecha')
    dn_buy = models.FloatField(verbose_name='Dolar Nación')
    dl_buy = models.FloatField(blank=True, null=True, default=None, verbose_name='Dolar Libre')
    dn_sell = models.FloatField(verbose_name='Dolar Nación')
    dl_sell = models.FloatField(blank=True, null=True, default=None, verbose_name='Dolar Libre')

    def __str__(self):
        return self.date.strftime('%m/%d/%Y')

    class Meta:
        verbose_name = 'Moneda'
        verbose_name_plural = 'Monedas'


class Board(models.Model):
    date = models.DateField(verbose_name='Fecha')
    wheat_ros = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo')
    wheat_bas = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo')
    wheat_qq = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo')
    wheat_bb = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo')
    wheat12_ros = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo Art. 12')
    wheat12_bas = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo Art. 12')
    wheat12_qq = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo Art. 12')
    wheat12_bb = models.FloatField(blank=True, null=True, default=None, verbose_name='Trigo Art. 12')
    corn_ros = models.FloatField(blank=True, null=True, default=None, verbose_name='Maiz')
    corn_bas = models.FloatField(blank=True, null=True, default=None, verbose_name='Maiz')
    corn_qq = models.FloatField(blank=True, null=True, default=None, verbose_name='Maiz')
    corn_bb = models.FloatField(blank=True, null=True, default=None, verbose_name='Maiz')
    sunflower_ros = models.FloatField(blank=True, null=True, default=None, verbose_name='Girasol')
    sunflower_bas = models.FloatField(blank=True, null=True, default=None, verbose_name='Girasol')
    sunflower_qq = models.FloatField(blank=True, null=True, default=None, verbose_name='Girasol')
    sunflower_bb = models.FloatField(blank=True, null=True, default=None, verbose_name='Girasol')
    soy_ros = models.FloatField(blank=True, null=True, default=None, verbose_name='Soja')
    soy_bas = models.FloatField(blank=True, null=True, default=None, verbose_name='Soja')
    soy_qq = models.FloatField(blank=True, null=True, default=None, verbose_name='Soja')
    soy_bb = models.FloatField(blank=True, null=True, default=None, verbose_name='Soja')
    sorghum_ros = models.FloatField(blank=True, null=True, default=None, verbose_name='Sorgo')
    sorghum_bas = models.FloatField(blank=True, null=True, default=None, verbose_name='Sorgo')
    sorghum_qq = models.FloatField(blank=True, null=True, default=None, verbose_name='Sorgo')
    sorghum_bb = models.FloatField(blank=True, null=True, default=None, verbose_name='Sorgo')

    def __str__(self):
        return self.date.strftime('%m/%d/%Y')

    class Meta:
        verbose_name = 'Pizarra'
        verbose_name_plural = 'Pizarras'


class City(models.Model):
    STATE_CHOICES = (
        ('BUE', 'Buenos Aires'),
        ('CHA', 'Chaco'),
    )
    city = models.CharField(max_length=80, verbose_name='Ciudad')
    state = models.CharField(max_length=3, choices=STATE_CHOICES, verbose_name='Provincia', default='BUE')

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'


class Rain(models.Model):
    date = models.DateField(verbose_name='Fecha', primary_key=True)

    def __str__(self):
        return self.date.strftime('%m/%d/%Y')

    class Meta:
        verbose_name = 'Lluvia'
        verbose_name_plural = 'Lluvias'


class RainDetail(models.Model):
    rain = models.ForeignKey(Rain, on_delete=models.CASCADE, verbose_name='Fecha')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Ciudad')
    mm = models.FloatField(verbose_name='Milimetros')

    def __str__(self):
        return self.city.city

    class Meta:
        verbose_name = 'Detalle'
        verbose_name_plural = 'Detalles'
        unique_together = (('rain', 'city'),)


class Notifications(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    title = models.CharField(max_length=200, verbose_name='Titulo')
    notification = models.TextField(verbose_name='Notificación')
    active = models.BooleanField(verbose_name='Activa/Inactiva', default=True)
    date_from = models.DateField(verbose_name='Vigencia Desde')
    date_to = models.DateField(verbose_name='Vigencia Hasta')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'


class ViewedNotifications(models.Model):
    notification = models.ForeignKey(Notifications, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed = models.BooleanField(verbose_name='Notificación vista', default=False)

    def __str__(self):
        return self.user.userinfo.company_name

    class Meta:
        verbose_name = 'Notificación por Usuario'
        verbose_name_plural = 'Notificaciones por Usuario'


class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    algoritmo_code = models.IntegerField(verbose_name='Cuenta Algoritmo')
    logged = models.DateTimeField(auto_now_add=True, verbose_name='Fecha/Hora de Ingreso')

    def __str__(self):
        return self.logged.strftime('%m/%d/%Y')

    class Meta:
        verbose_name = 'Log de Acceso'
        verbose_name_plural = 'Log de Acceso'


class Careers(models.Model):
    title = models.CharField(verbose_name='Título', max_length=80)
    active = models.BooleanField(verbose_name='Activo / Inactivo')
    description = models.TextField(verbose_name='Descripción')
    requirements = models.TextField(verbose_name='Requerimientos')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Oportunidad Laboral'
        verbose_name_plural = 'Oportunidades Laborales'