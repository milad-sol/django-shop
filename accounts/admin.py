from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserCreationForm, UserChangeForm
from .models import User, OtpCode


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    readonly_fields = ('last_login',)
    fieldsets = [('Main', {'fields': ['email', 'phone_number', 'full_name', 'password']}),
                 ('Permissions',
                  {'fields': ('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
                 ]

    add_fieldsets = [
        ('None', {
            'fields': ['phone_number', 'email', 'full_name', 'password', 'confirm_password']
        })
    ]
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ('groups', 'user_permissions')


# admin.site.unregister(Group)
admin.site.register(User, UserAdmin)


@admin.register(OtpCode)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ['phone', 'code', 'created']
