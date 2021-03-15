from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OidcClientConfig(AppConfig):
    name = 'app.oidc_client'
    verbose_name = _('openid management')

    def ready(self):
        import app.oidc_client.signals
