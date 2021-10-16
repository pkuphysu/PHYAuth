from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from guardian.admin import GuardedModelAdmin
from oidc_provider.admin import ClientForm
from oidc_provider.models import Client

from .models import Faq, ClientGroup, ClientUserMemberShip

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


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'get_show_display', 'rank']
    search_fields = ['question', 'answer']
    list_filter = ['show']


@admin.register(ClientGroup)
class ClientGroupAdmin(admin.ModelAdmin):
    list_display = ['owner', 'name']
    search_fields = ['owner__username', 'owner__name', 'name']


@admin.register(ClientUserMemberShip)
class MemberShipAdmin(admin.ModelAdmin):
    list_display = ['group', 'user', 'inviter', 'invite_time', 'date_joined', 'remark']
    search_fields = ['group__name', 'user__username', 'user__name', 'inviter__username', 'inviter__name']
