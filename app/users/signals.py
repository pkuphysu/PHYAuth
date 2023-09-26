import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .tasks import user_register_email, user_active_update_email
from ..pku_iaaa.signals import iaaa_user_create, iaaa_user_login_success


UserModel = get_user_model()
logger = logging.getLogger(__name__)


@receiver(iaaa_user_create)
def user_create_send_email(sender, user, **kwargs):
    user_register_email.delay(user_id=user.id)


@receiver(iaaa_user_login_success)
def update_last_iaaa_login(sender, user, **kwargs):
    """
    A signal receiver which updates the last_iaaa_login date for
    the user logging in by iaaa.
    """
    user.last_iaaa_login = timezone.now()
    user.save(update_fields=['last_iaaa_login'])


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_create(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        user.add_obj_perm('change_user', user)
        user.add_obj_perm('view_user', user)


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def user_active_update(sender, **kwargs):
    if kwargs['instance'].id:
        user = kwargs['instance']
        o_user = get_user_model().objects.get(id=user.id)
        if not o_user.is_active and user.is_active:
            user_active_update_email.delay(user.id)
            logger.info(f'user {user.username} is marked as active!')
