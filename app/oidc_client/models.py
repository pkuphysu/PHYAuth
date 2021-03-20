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
