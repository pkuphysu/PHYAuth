from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import user_register_email
from ..pku_iaaa.signals import iaaa_user_create


@receiver(iaaa_user_create)
def user_create_send_email(sender, **kwargs):
    user_register_email.delay(user_id=kwargs['user_id'])


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_create(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        user.add_obj_perm('change_user', user)
        user.add_obj_perm('view_user', user)
