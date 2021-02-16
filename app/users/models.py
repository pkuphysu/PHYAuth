from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import UsernameValidator, PKUEmailValidator


class User(AbstractUser):
    username_validator = UsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=10,
        unique=True,
        help_text=_('Required. It\'s your pku id. 10 characters. Digits only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        _('pku email address'),
        validators=[PKUEmailValidator()],
        help_text=_('This is your pku email address, because some clients only require email address.')
    )

    nickname = models.CharField(
        _('nickname'),
        max_length=50,
        blank=True
    )

    website = models.CharField(
        _('website'),
        max_length=100,
        blank=True
    )

    gender = models.SmallIntegerField(
        _('gender'),
        choices=(
            (0, _('unknown')),
            (1, _('male')),
            (2, _('female'))
        ),
        default=0
    )

    birthdate = models.DateField(
        _('birthdate'),
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        _('phone number'),
        max_length=15,
        blank=True
    )

    address = models.CharField(
        _('address'),
        max_length=50,
        blank=True
    )

    preferred_email = models.EmailField(
        _('preferred email address'),
        blank=True,
        help_text=_('This is your usual email address which we will use to get in touch with you.')
    )

    is_teacher = models.BooleanField(
        _('is teacher'),
        choices=((False, '学生'), (True, '教职工')),
        default=False,
        help_text=_(
            'Designates whether the user is a teacher.'
        )
    )

    is_banned = models.BooleanField(
        _('is banned'),
        choices=(
            (False, '正常'),
            (True, '封禁')
        ),
        default=False,
        help_text=_('Designate whether the user is banned.')
    )

    in_school = models.BooleanField(
        _('is in school'),
        default=True,
        choices=(
            (False, '离校、离职'),
            (True, '在校、在职')
        ),
        help_text=_('Designate whether the user is in school.')
    )

    REQUIRED_FIELDS = ['email']

    class Meta(AbstractUser.Meta):
        pass

    def get_email(self):
        if self.is_teacher:
            return self.username + '@pku.edu.cn'
        elif int(self.username[0]) < 2:
            return self.username + '@pku.edu.cn'
        else:
            return self.username + '@stu.pku.edu.cn'

    def get_preferred_email(self):
        if self.preferred_email:
            return self.preferred_email
        else:
            return self.email
