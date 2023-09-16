from django.db import models
from django.contrib.auth.models import User

from tinymce.models import HTMLField


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


class Notifications(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    title = models.CharField(max_length=200, verbose_name='Titulo')
    notification = HTMLField(verbose_name='Notificación')
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


class IncomeQuality(models.Model):
    species = models.CharField(max_length=4, verbose_name='Especie')
    harvest = models.CharField(max_length=4, verbose_name='Cosecha')
    ticket = models.CharField(max_length=16, verbose_name='Ticket')
    income = models.CharField(max_length=16, verbose_name='Ingreso')
    cp = models.CharField(max_length=16, verbose_name='Carta de Porte')
    algoritmo_code = models.IntegerField(verbose_name='Cuenta Algoritmo')               # 100712 EL PIGUEL S.A.
    name = models.CharField(max_length=150, verbose_name='Razón Social')
    field = models.IntegerField(verbose_name='Campo')                                   # 469 EL EMBARCADERO
    field_description = models.CharField(max_length=100, verbose_name='Nombre de Campo')
    gross_kg = models.IntegerField(verbose_name='Peso Bruto')
    tare = models.IntegerField(verbose_name='Tara')
    net_weight = models.IntegerField(verbose_name='Peso Neto')
    humidity_percentage = models.FloatField(verbose_name='Humedad (%)')
    humidity_volatile_reduction = models.FloatField(verbose_name='Merma de Humedad + Volatil')
    humidity_volatile_kg = models.IntegerField(verbose_name='Kilos de Humedad + Volatil')
    dry_kg = models.IntegerField(verbose_name='Kilos Secos')
    quality_percentage = models.FloatField(verbose_name='Calidad (%)')
    conditioning_kg = models.IntegerField(verbose_name='Kilos Acondicionamiento')
    item_1 = models.FloatField(verbose_name='Rubro 1')
    item_2 = models.FloatField(verbose_name='Rubro 2')
    item_3 = models.FloatField(verbose_name='Rubro 3')
    item_4 = models.FloatField(verbose_name='Rubro 4')
    item_5 = models.FloatField(verbose_name='Rubro 5')
    item_6 = models.FloatField(verbose_name='Rubro 6')
    item_7 = models.FloatField(verbose_name='Rubro 7')
    item_8 = models.FloatField(verbose_name='Rubro 8')
    item_9 = models.FloatField(verbose_name='Rubro 9')
    item_10 = models.FloatField(verbose_name='Rubro 10')
    item_11 = models.FloatField(verbose_name='Rubro 11')
    item_12 = models.FloatField(verbose_name='Rubro 12')
    item_13 = models.FloatField(verbose_name='Rubro 13')
    item_14 = models.FloatField(verbose_name='Rubro 14')
    item_15 = models.FloatField(verbose_name='Rubro 15')
    plant = models.IntegerField(verbose_name='Planta')               # 1 Elevador Arrecifes
    plant_description = models.CharField(max_length=150, verbose_name='Descripción Planta')
    shaking_reduction = models.FloatField(verbose_name='Merma de Zarandeo')
    shaking_kg = models.IntegerField(verbose_name='Kilos de Zarandeo')
    volatile_percentage = models.FloatField(verbose_name='Porcentaje Volatil')
    volatile_kg = models.IntegerField(verbose_name='Kilos Volatil')
    quality_reduction = models.IntegerField(verbose_name='Merma de Calidad')
    grade = models.IntegerField(verbose_name='Grado')
    factor = models.FloatField(verbose_name='Factor')
    speciesharvest = models.CharField(max_length=8, verbose_name='Especie Cosecha', null=True)
    bonus_item_1 = models.FloatField(verbose_name='Bonificación Rubro 1')
    bonus_item_2 = models.FloatField(verbose_name='Bonificación Rubro 2')
    bonus_item_3 = models.FloatField(verbose_name='Bonificación Rubro 3')
    bonus_item_4 = models.FloatField(verbose_name='Bonificación Rubro 4')
    bonus_item_5 = models.FloatField(verbose_name='Bonificación Rubro 5')
    bonus_item_6 = models.FloatField(verbose_name='Bonificación Rubro 6')
    bonus_item_7 = models.FloatField(verbose_name='Bonificación Rubro 7')
    bonus_item_8 = models.FloatField(verbose_name='Bonificación Rubro 8')
    bonus_item_9 = models.FloatField(verbose_name='Bonificación Rubro 9')
    bonus_item_10 = models.FloatField(verbose_name='Bonificación Rubro 10')
    bonus_item_11 = models.FloatField(verbose_name='Bonificación Rubro 11')
    bonus_item_12 = models.FloatField(verbose_name='Bonificación Rubro 12')
    bonus_item_13 = models.FloatField(verbose_name='Bonificación Rubro 13')
    bonus_item_14 = models.FloatField(verbose_name='Bonificación Rubro 14')
    bonus_item_15 = models.FloatField(verbose_name='Bonificación Rubro 15')
    reduction_item_1 = models.FloatField(verbose_name='Rebaja Rubro 1')
    reduction_item_2 = models.FloatField(verbose_name='Rebaja Rubro 2')
    reduction_item_3 = models.FloatField(verbose_name='Rebaja Rubro 3')
    reduction_item_4 = models.FloatField(verbose_name='Rebaja Rubro 4')
    reduction_item_5 = models.FloatField(verbose_name='Rebaja Rubro 5')
    reduction_item_6 = models.FloatField(verbose_name='Rebaja Rubro 6')
    reduction_item_7 = models.FloatField(verbose_name='Rebaja Rubro 7')
    reduction_item_8 = models.FloatField(verbose_name='Rebaja Rubro 8')
    reduction_item_9 = models.FloatField(verbose_name='Rebaja Rubro 9')
    reduction_item_10 = models.FloatField(verbose_name='Rebaja Rubro 10')
    reduction_item_11 = models.FloatField(verbose_name='Rebaja Rubro 11')
    reduction_item_12 = models.FloatField(verbose_name='Rebaja Rubro 12')
    reduction_item_13 = models.FloatField(verbose_name='Rebaja Rubro 13')
    reduction_item_14 = models.FloatField(verbose_name='Rebaja Rubro 14')
    reduction_item_15 = models.FloatField(verbose_name='Rebaja Rubro 15')
    services_kg = models.IntegerField(verbose_name='Kilos Servicio')
    gluten = models.IntegerField(verbose_name='Gluten')
    fumigation_charge = models.CharField(max_length=30, verbose_name='Cobro de Fumigado')
    quality_datetime = models.DateTimeField(null=True, verbose_name='Fecha y Hora de Calidad')

    def __str__(self):
        return self.ticket
    class Meta:
        verbose_name = 'Calidad de Ingresos'


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
    external_voucher_number = models.BigIntegerField(verbose_name='Numero Comprobante Externo')
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
    external_voucher_number = models.BigIntegerField(verbose_name='Numero Comprobante Externo')
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
    cta_cte = models.CharField(max_length=80, verbose_name='Tipo Cta. Cte.')
    cta_cte_name = models.CharField(max_length=80, verbose_name='Descripcion Cta. Cte.')

    def __str__(self):
        return self.voucher

    class Meta:
        verbose_name = 'Cuenta Corriente'
        verbose_name_plural = 'Cuentas Corrientes'


class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    algoritmo_code = models.IntegerField(verbose_name='Cuenta Algoritmo')
    logged = models.DateTimeField(auto_now_add=True, verbose_name='Fecha/Hora de Ingreso')

    def __str__(self):
        return self.logged.strftime('%m/%d/%Y')

    class Meta:
        verbose_name = 'Log de Acceso'
        verbose_name_plural = 'Log de Acceso'
