from django.apps import AppConfig


class ApplyConfig(AppConfig):
    name = 'app.apply'

    def ready(self):
        import app.apply.signals
