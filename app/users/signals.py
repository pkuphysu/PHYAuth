from django.contrib.auth import get_user_model
from django.dispatch import receiver
from oidc_provider.signals import user_accept_consent

from ..pku_iaaa.signals import user_create
from .tasks import consent_accept_email, user_register_email

UserModel = get_user_model()


@receiver(user_accept_consent)
def user_accept_consent_send_email(sender, **kwargs):
    consent_accept_email.delay(client_id=kwargs['client'].id,
                               user_id=kwargs['user'].id,
                               scope=kwargs['scope'])


@receiver(user_create)
def user_create_send_email(sender, **kwargs):
    user_register_email.delay(user_id=kwargs['user_id'])
