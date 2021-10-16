from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from oidc_provider.models import Client


class Faq(models.Model):
    question = models.CharField(
        _('question'),
        max_length=200,
    )

    answer = models.TextField(
        _('answer'),
    )

    show = models.BooleanField(
        _('show'),
        choices=(
            (False, _('Hide')),
            (True, _('Show'))
        ),
        default=True
    )
    rank = models.PositiveSmallIntegerField(
        _('faq order'),
        help_text=_('It is the default order of the faq!\n'
                    'The smaller it is, the more front it will be.\n'
                    'If some are the same, the earlier create one will appear firstly.')
    )

    class Meta:
        verbose_name = _('oidc faq')
        verbose_name_plural = _('oidc faqs')


class ClientGroup(models.Model):
    name = models.CharField(_('group name'), max_length=150, unique=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('users'),
        help_text=_(
            'The users belong to this group.'
        ),
        through='ClientUserMemberShip',
        through_fields=('group', 'user')
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name=_('client')
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('owner'),
        related_name='own_app_group_set'
    )

    class Meta:
        verbose_name = _('client group')
        verbose_name_plural = _('client groups')

    def __str__(self):
        return self.name


class ClientUserMemberShip(models.Model):
    group = models.ForeignKey(ClientGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='membership_invites')
    invite_time = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('group', 'user',)
        verbose_name = _('membership')
        verbose_name_plural = _('memberships')
