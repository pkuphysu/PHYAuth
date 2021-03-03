from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PortalConfig(AppConfig):
    name = 'app.portal'
    verbose_name = _('portal management')

    def ready(self):
        import app.portal.signals
