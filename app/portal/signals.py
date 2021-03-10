import logging

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TopLink, Announcement

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Announcement)
def announcement_create(sender, **kwargs):
    if kwargs['created']:
        announcement = kwargs['instance']
        user = announcement.owner
        user.add_obj_perm('change_announcement', announcement)
        user.add_obj_perm('view_announcement', announcement)
        user.add_obj_perm('delete_announcement', announcement)
        logger.info(f'Add obj perm of announcement {announcement.id} to user {user.username}')


@receiver(post_save, sender=TopLink)
def toplink_create(sender, **kwargs):
    if kwargs['created']:
        toplink = kwargs['instance']
        user = toplink.owner
        user.add_obj_perm('change_toplink', toplink)
        user.add_obj_perm('view_toplink', toplink)
        user.add_obj_perm('delete_toplink', toplink)
        logger.info(f'Add obj perm of announcement {toplink.id} to user {user.username}')


@receiver(post_save, sender=TopLink)
def toplink_update(sender, **kwargs):
    key = make_template_fragment_key('nav_top_links')
    cache.delete(key)
    logger.info(f'Delete nav_top_links cache.')
