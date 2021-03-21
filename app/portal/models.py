from django.db import models
from django.utils.translation import gettext_lazy as _


class TopLink(models.Model):
    name = models.CharField(
        _('Link Name'),
        max_length=32,
    )
    url = models.URLField(
        _('Link URL'),
        max_length=100
    )
    rank = models.PositiveSmallIntegerField(
        _('Link Rank'),
        help_text=_('It is the default order of the links, they should not be same!\n'
                    'The smaller it is, the more front it will be.\n'
                    'If some are the same, the earlier create one will appear firstly.')
    )

    class Meta:
        verbose_name = _('Top Link')
        verbose_name_plural = _('Top Links')


class Announcement(models.Model):
    title = models.CharField(
        _('Announcement Title'),
        max_length=100,
    )

    content = models.TextField(
        _('Announcement Content'),
    )

    rank = models.PositiveSmallIntegerField(
        _('Announcement Rank'),
        help_text=_('It is the default order of the announcement!\n'
                    'The smaller it is, the more front it will be.\n'
                    'If some are the same, the later create one will appear firstly.')
    )

    class Meta:
        verbose_name = _('Announcement')
        verbose_name_plural = _('Announcements')
