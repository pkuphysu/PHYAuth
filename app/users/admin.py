from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdmin(AbstractUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': (
            'first_name', 'last_name', 'nickname', 'email', 'gender',
            'birthdate', 'phone_number', 'address', 'website'
        )}),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_teacher', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Account Status'), {'fields': ('is_active', 'is_banned')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )

    list_display = ('username', 'first_name', 'last_name', 'nickname', 'email', 'is_teacher', 'is_staff')
    list_filter = ('is_teacher', 'is_staff', 'is_superuser', 'is_active', 'groups', 'is_banned')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'nickname')


admin.site.register(User, UserAdmin)
