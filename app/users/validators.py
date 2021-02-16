from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^[0-9]{10}\Z'
    message = _('Enter a valid username. It\'s your pku id. This value may contain only numbers.')
    flags = 0


@deconstructible
class PKUEmailValidator(validators.RegexValidator):
    regex = r'^[0-9]{10}@((stu|alumni)\.)?pku.edu.cn\Z'
    message = _('Enter your ID email address, it should be in 2000000000@(stu.|alumni.)pku.edu.cn format.')
    flags = 0
