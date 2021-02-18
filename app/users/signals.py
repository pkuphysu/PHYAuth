from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from oidc_provider.signals import user_accept_consent

from .tasks import consent_accept_email

UserModel = get_user_model()


@receiver(user_accept_consent)
def user_accept_consent_send_email(sender, **kwargs):
    consent_accept_email.delay(client_id=kwargs['client'].id,
                               user_id=kwargs['user'].id,
                               scope=kwargs['scope'])
    # print(kwargs)
    # print('Ups! Some user has declined the consent.')

# @receiver(post_save, sender=UserModel)
# def user_create(sender, **kwargs):
#     if kwargs['created']:
#
#         print(kwargs)
#         print('Ups! A user has been created')
#     else:
#         pass
