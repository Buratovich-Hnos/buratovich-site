from django.db import models


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
