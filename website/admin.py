from django.contrib import admin
from django.utils.safestring import mark_safe

from website.models import Currencies
from website.models import Board
from website.models import City
from website.models import Rain
from website.models import RainDetail
from website.models import Careers

from website.forms import CareerCreationForm


class CurrenciesAdmin(admin.ModelAdmin):
    list_display = ('date', 'get_dn_buy', 'get_dn_sell', 'get_dl_buy', 'get_dl_sell',)
    empty_value_display = ''
    date_hierarchy = 'date'

    fieldsets = (
        (None, {
            'fields': ('date',),
        }),
        ('Compra', {
            'fields': (('dn_buy', 'dl_buy'),),
        }),
        ('Venta', {
            'fields': (('dn_sell', 'dl_sell'),),
        }),
    )

    def get_dn_buy(self, obj):
        return obj.dn_buy

    def get_dn_sell(self, obj):
        return obj.dn_sell

    def get_dl_buy(self, obj):
        return obj.dl_buy

    def get_dl_sell(self, obj):
        return obj.dl_sell

    get_dn_buy.short_description = 'Nación Compra'
    get_dn_sell.short_description = 'Nación Venta'
    get_dl_buy.short_description = 'Libre Compra'
    get_dl_sell.short_description = 'Libre Venta'
    get_dn_buy.admin_order_field = 'dn_buy'
    get_dn_sell.admin_order_field = 'dn_sell'
    get_dl_buy.admin_order_field = 'dl_buy'
    get_dl_sell.admin_order_field = 'dl_sell'


class BoardAdmin(admin.ModelAdmin):
    list_display = ('date',)
    empty_value_display = ''
    date_hierarchy = 'date'

    fieldsets = (
        (None, {
            'fields': ('date',),
        }),
        ('Rosario', {
            'classes': ('species',),
            'fields': (('wheat_ros', 'corn_ros', 'sunflower_ros', 'soy_ros', 'sorghum_ros'),),
        }),
        ('Buenos Aires', {
            'classes': ('species',),
            'fields': (('wheat_bas', 'corn_bas', 'sunflower_bas', 'soy_bas', 'sorghum_bas'),),
        }),
        ('Bahia Blanca', {
            'classes': ('species',),
            'fields': (('wheat_bb', 'corn_bb', 'sunflower_bb', 'soy_bb', 'sorghum_bb'),),
        }),
        ('Quequen', {
            'classes': ('species',),
            'fields': (('wheat_qq', 'corn_qq', 'sunflower_qq', 'soy_qq', 'sorghum_qq'),),
        }),
    )

    class Media:
        css = {
            'all': ('css/board.css',)
        }


class RainDetailInline(admin.StackedInline):
    model = RainDetail
    can_delete = False
    extra = 1
    verbose_name = 'Detalle de Lluvia'
    verbose_name_plural = 'Detalle de Lluvias'

    inline_classes = ('grp-collapse grp-open',)


class RainAdmin(admin.ModelAdmin):
    inlines = (RainDetailInline, )
    date_hierarchy = 'date'


class CityAdmin(admin.ModelAdmin):
    list_display = ('city', 'state',)
    empty_value_display = ''


class CareersAdmin(admin.ModelAdmin):
    form = CareerCreationForm
    list_display = ('title', 'active', 'description_html', 'requirements_html',)

    def description_html(self, obj):
        return mark_safe(obj.description)

    def requirements_html(self, obj):
        return mark_safe(obj.requirements)

    description_html.allow_tags = True
    requirements_html.allow_tags = True
    description_html.short_description = 'Descripción'
    requirements_html.short_description = 'Requerimientos'


# Register models
admin.site.register(Currencies, CurrenciesAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Rain, RainAdmin)
admin.site.register(Careers, CareersAdmin)
