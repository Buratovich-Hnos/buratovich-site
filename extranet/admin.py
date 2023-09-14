from django.contrib import admin
from django.utils.safestring import mark_safe

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from extranet.forms import UserCreationForm, NotificationCreationForm
from extranet.models import UserInfo, Notifications, ViewedNotifications, AccessLog


# Unregister models
admin.site.unregister(User)


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


class NotificationsAdmin(admin.ModelAdmin):
    form = NotificationCreationForm
    list_display = ('title', 'notifications_html', 'active', 'date_from', 'date_to',)

    def notifications_html(self, obj):
        return mark_safe(obj.notification)

    notifications_html.allow_tags = True
    notifications_html.short_description = 'Notificación'


class ViewedNotificationsAdmin(admin.ModelAdmin):
    list_display = ('get_company_name', 'notification',)

    def get_company_name(self, obj):
        return obj.user.userinfo.company_name

    get_company_name.short_description = 'Razón Social'
    get_company_name.admin_order_field = 'user__userinfo__company_name'


class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'algoritmo_code', 'logged')
    list_filter = ('user', 'algoritmo_code', 'logged')



# Register models
admin.site.register(User, UserAdmin)
admin.site.register(Notifications, NotificationsAdmin)
admin.site.register(ViewedNotifications, ViewedNotificationsAdmin)
admin.site.register(AccessLog, AccessLogAdmin)