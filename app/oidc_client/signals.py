import logging

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from oidc_provider.models import Client
from oidc_provider.signals import user_accept_consent

from .models import Faq, ClientGroup, ClientUserMemberShip
from .tasks import consent_accept_email, clientgroup_invite_user_email

logger = logging.getLogger(__name__)


@receiver(user_accept_consent)
def user_accept_consent_send_email(sender, **kwargs):
    consent_accept_email.delay(client_id=kwargs['client'].id,
                               user_id=kwargs['user'].id,
                               scope=kwargs['scope'])


@receiver(post_save, sender=Client)
def client_create(sender, **kwargs):
    if kwargs['created']:
        client = kwargs['instance']
        user = client.owner
        user.add_obj_perm('view_client', client)
        user.add_obj_perm('change_client', client)


@receiver(post_save, sender=ClientGroup)
def client_group_create(sender, **kwargs):
    if kwargs['created']:
        group = kwargs['instance']
        user = group.owner
        user.add_obj_perm('view_clientgroup', group)
        user.add_obj_perm('change_clientgroup', group)
        user.add_obj_perm('delete_clientgroup', group)


@receiver(pre_save, sender=ClientGroup)
def client_group_update(sender, **kwargs):
    if kwargs['instance'].id:
        group = kwargs['instance']
        o_group = ClientGroup.objects.get(id=group.id)
        if o_group.owner != group.owner:
            user = group.owner
            user.add_obj_perm('view_clientgroup', group)
            user.add_obj_perm('change_clientgroup', group)
            user.add_obj_perm('delete_clientgroup', group)
            o_user = o_group.owner
            o_user.del_obj_perm('view_clientgroup', group)
            o_user.del_obj_perm('change_clientgroup', group)
            o_user.del_obj_perm('delete_clientgroup', group)
            logger.info(f'Client Group {group.id} {group.name} change owner from {o_user.username} to {user.username}.')


@receiver(post_save, sender=ClientUserMemberShip)
def membership_create(sender, **kwargs):
    if kwargs['created']:
        ms = kwargs['instance']
        clientgroup_invite_user_email.delay(ms.id)


@receiver(post_delete, sender=Faq)
@receiver(post_save, sender=Faq)
def oidc_client_faq_update(sender, **kwargs):
    key = make_template_fragment_key('oidc_client_faq_page')
    cache.delete(key)
    logger.info(f'Delete oidc_client_faq_page cache.')
