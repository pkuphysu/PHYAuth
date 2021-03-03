from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TopLink(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True, default=None,
        verbose_name=_('Owner'),
        related_name='toplink_set'
    )
    name = models.CharField(
        _('Link Name'),
        max_length=32,
    )
    url = models.URLField(
        _('Link URL'),
        max_length=100
    )
    rank = models.SmallIntegerField(
        _('Link Rank'),
        help_text=_('It is the default order of the links, they should not be same!\n'
                    'The smaller it is, the more front it will be.\n'
                    'If some are the same, the earlier create one will appear firstly.')
    )

    class Meta:
        verbose_name = _('Top Link')
        verbose_name_plural = _('Top Links')


class Announcement(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True, default=None,
        verbose_name=_('Owner'),
        related_name='announcement_set'
    )
    type = models.CharField(
        _('Announcement Type'),
        max_length=20,
        choices=(
            ('success', _('success')),
            ('warning', _('warning')),
            ('info', _('info')),
            ('danger', _('danger')),
        ),
        help_text=_('success-green, warning-yellow, info-blue, danger-red')
    )

    title = models.CharField(
        _('Announcement Title'),
        max_length=100,
    )

    content = models.TextField(
        _('Announcement Content'),
    )

    rank = models.SmallIntegerField(
        _('Announcement Rank'),
        help_text=_('It is the default order of the announcement!\n'
                    'The smaller it is, the more front it will be.\n'
                    'If some are the same, the later create one will appear firstly.')
    )

    class Meta:
        verbose_name = _('Announcement')
        verbose_name_plural = _('Announcements')
