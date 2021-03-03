from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TopLink, Announcement


@receiver(post_save, sender=Announcement)
def announcement_create(sender, **kwargs):
    if kwargs['created']:
        announcement = kwargs['instance']
        user = announcement.owner
        user.add_obj_perm('change_announcement', announcement)
        user.add_obj_perm('view_announcement', announcement)
        user.add_obj_perm('delete_announcement', announcement)


@receiver(post_save, sender=TopLink)
def client_create(sender, **kwargs):
    if kwargs['created']:
        toplink = kwargs['instance']
        user = toplink.owner
        user.add_obj_perm('change_toplink', toplink)
        user.add_obj_perm('view_toplink', toplink)
        user.add_obj_perm('delete_toplink', toplink)
