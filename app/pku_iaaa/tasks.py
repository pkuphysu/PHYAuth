from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template import loader

from PHYAuth.celery import TransactionAwareTask, my_send_mail

UserModel = get_user_model()


@shared_task(base=TransactionAwareTask)
def user_register_email(user_id):
    domain = settings.DOMAIN + settings.SUBPATH

    user = UserModel.objects.get(id=user_id)

    from_email = settings.EMAIL_FROM
    subject = '欢迎注册物理学院统一身份认证系统'
    tea_html = loader.render_to_string(
        'email/users/register.html',
        {
            'domain': domain,
            'name': user.last_name + user.first_name,
        }
    )
    my_send_mail.delay(subject, tea_html, from_email, [user.get_preferred_email()])
