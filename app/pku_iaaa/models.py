from django.db import models
from django.utils.translation import gettext_lazy as _


class Iaaa(models.Model):
    app_id = models.CharField(
        _('APP ID'),
        max_length=50,
        unique=True,
        help_text=_('Required. Please connect pkucc for help.')
    )

    key = models.CharField(
        _('KEY'),
        max_length=50,
        help_text=_('Required. Please connect pkucc for help.')
    )

    redirect_url = models.CharField(
        _('REDIRECT URL'),
        max_length=200,
        help_text=_('Required. Please connect pkucc for help.')
    )

    class Meta:
        verbose_name = _('IAAA Info')
        verbose_name_plural = verbose_name
