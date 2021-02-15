from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^[0-9]{10}\Z'
    message = 'Enter a valid username. It\'s your pku id. This value may contain only numbers.'
    flags = 0
