from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


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


class AppGroup(models.Model):
    name = models.CharField(_('group name'), max_length=150, unique=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('app groups'),
        blank=True,
        help_text=_(
            'The users belong to this group.'
        ),
        related_name="app_group_set",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('owner'),
        related_name='own_app_group_set'
    )

    class Meta:
        verbose_name = _('app group')
        verbose_name_plural = _('app groups')


