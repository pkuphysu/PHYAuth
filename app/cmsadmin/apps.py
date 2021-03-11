from django.apps import AppConfig


class CmsadminConfig(AppConfig):
    name = 'app.cmsadmin'

    def ready(self):
        import app.cmsadmin.signals
