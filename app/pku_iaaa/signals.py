from django.dispatch import Signal

user_create = Signal(providing_args=['user_id'])
