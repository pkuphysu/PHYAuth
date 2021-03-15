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

    class Meta:
        verbose_name = _('oidc faq')
        verbose_name_plural = _('oidc faqs')
