import logging

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import TopLink, Announcement

logger = logging.getLogger(__name__)


@receiver(post_delete, sender=TopLink)
@receiver(post_save, sender=TopLink)
def toplink_update(sender, **kwargs):
    key = make_template_fragment_key('nav_top_links')
    cache.delete(key)
    logger.info(f'Delete nav_top_links cache.')


@receiver(post_delete, sender=Announcement)
@receiver(post_save, sender=Announcement)
def toplink_update(sender, **kwargs):
    key = make_template_fragment_key('index_announcements')
    cache.delete(key)
    logger.info(f'Delete index_announcements cache.')
