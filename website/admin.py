from django.contrib import admin

from website.forms import UserCreationForm

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from website.models import UserInfo


# Unregister models
admin.site.unregister(User)
admin.site.unregister(Group)


class UserInline(admin.StackedInline):
    model = UserInfo
    can_delete = False
    verbose_name = 'Informacion Algoritmo'
    verbose_name_plural = 'Informacion Algoritmo'
    exclude = ('account_confirmed', 'random_password', 'is_commercial')

    inline_classes = ('grp-collapse grp-open',)


class UserAdmin(BaseUserAdmin):
    inlines = (UserInline, )
    add_form = UserCreationForm

    list_display = ('username', 'email', 'get_company_name', 'get_algoritmo_code', 'get_is_commercial', 'is_active', 'is_staff',)
    empty_value_display = ''

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email',)}
        ),
    )

    def get_is_commercial(self, obj):
        return obj.userinfo.is_commercial

    def get_company_name(self, obj):
        return obj.userinfo.company_name

    def get_algoritmo_code(self, obj):
        return obj.userinfo.algoritmo_code

    get_is_commercial.boolean = True
    get_is_commercial.short_description = 'Es Comercial'
    get_company_name.short_description = 'Razón Social'
    get_algoritmo_code.short_description = 'Código Algoritmo'
    get_is_commercial.admin_order_field = 'userinfo__is_commercial'
    get_company_name.admin_order_field = 'userinfo__company_name'
    get_algoritmo_code.admin_order_field = 'userinfo__algoritmo_code'


# Register models
admin.site.register(User, UserAdmin)