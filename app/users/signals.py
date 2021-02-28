from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from oidc_provider.signals import user_accept_consent

from ..pku_iaaa.signals import iaaa_user_create
from .tasks import consent_accept_email, user_register_email


@receiver(user_accept_consent)
def user_accept_consent_send_email(sender, **kwargs):
    consent_accept_email.delay(client_id=kwargs['client'].id,
                               user_id=kwargs['user'].id,
                               scope=kwargs['scope'])


@receiver(iaaa_user_create)
def user_create_send_email(sender, **kwargs):
    user_register_email.delay(user_id=kwargs['user_id'])


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_create(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        user.add_obj_perm('change_user', user)
        user.add_obj_perm('view_user', user)
