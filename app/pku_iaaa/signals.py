from django.dispatch import Signal

iaaa_user_create = Signal(providing_args=['user_id'])
iaaa_user_login_success = Signal(providing_args=['user'])
iaaa_user_login_fail = Signal(providing_args=['user'])
