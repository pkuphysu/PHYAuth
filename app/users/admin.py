from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin
from django.utils.translation import gettext_lazy as _
from guardian.admin import GuardedModelAdmin

from .models import User, Department


@admin.register(Department)
class DepartmentAdmin(GuardedModelAdmin):
    list_display = ['department']


@admin.register(User)
class UserAdmin(AbstractUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': (
            'name',
            'first_name', 'last_name', 'nickname', 'email', 'preferred_email', 'department',
            'gender', 'birthdate', 'phone_number', 'address', 'website', 'introduce'
        )}),
        (_('Permissions'), {
            'fields': ('is_admin', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important Dates'), {'fields': ('last_login', 'last_iaaa_login', 'date_joined')}),
        (_('Account Status'), {'fields': ('is_active', 'is_teacher', 'in_school')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )

    list_display = ('username', 'name', 'nickname', 'email', 'is_admin', 'is_teacher', 'in_school')
    list_filter = ('is_teacher', 'is_admin', 'is_staff', 'is_superuser', 'is_active', 'groups', 'department')
    search_fields = ('username', 'name', 'email', 'nickname')
