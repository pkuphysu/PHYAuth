from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin
from django.utils.translation import gettext_lazy as _
from guardian.admin import GuardedModelAdmin
from oidc_provider.admin import ClientForm
from oidc_provider.models import Client

from .models import User, Department


@admin.register(Department)
class DepartmentAdmin(GuardedModelAdmin):
    list_display = ['department']


class UserAdmin(AbstractUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': (
            'name',
            'first_name', 'last_name', 'nickname', 'email', 'preferred_email', 'department',
            'gender', 'birthdate', 'phone_number', 'address', 'website', 'introduce'
        )}),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Account Status'), {'fields': ('is_active', 'is_teacher', 'in_school')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )

    list_display = ('username', 'name', 'nickname', 'email', 'is_teacher', 'in_school')
    list_filter = ('is_teacher', 'is_staff', 'is_superuser', 'is_active', 'groups', 'department')
    search_fields = ('username', 'name', 'email', 'nickname')


admin.site.register(User, UserAdmin)
admin.site.unregister(Client)


@admin.register(Client)
class ClientAdmin(GuardedModelAdmin):
    fieldsets = [
        [_(u'Base'), {
            'fields': (
                'name', 'owner', 'client_type', 'response_types', '_redirect_uris', 'jwt_alg',
                'require_consent', 'reuse_consent'),
        }],
        [_(u'Credentials'), {
            'fields': ('client_id', 'client_secret', '_scope'),
        }],
        [_(u'Information'), {
            'fields': ('contact_email', 'website_url', 'terms_url', 'logo', 'date_created'),
        }],
        [_(u'Session Management'), {
            'fields': ('_post_logout_redirect_uris',),
        }],
    ]
    form = ClientForm
    list_display = ['name', 'client_id', 'response_type_descriptions', 'date_created']
    readonly_fields = ['date_created']
    search_fields = ['name']
    raw_id_fields = ['owner']
