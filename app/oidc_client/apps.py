from django.apps import AppConfig


class OidcClientConfig(AppConfig):
    name = 'app.oidc_client'

    def ready(self):
        import app.oidc_client.signals
