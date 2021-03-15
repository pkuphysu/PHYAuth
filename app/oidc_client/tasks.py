from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template import loader
from oidc_provider.models import Client

from PHYAuth.celery import TransactionAwareTask, my_send_mail
from ..utils.oidc import get_scopes_information

UserModel = get_user_model()


@shared_task(base=TransactionAwareTask)
def consent_accept_email(user_id, client_id, scope):
    domain = settings.DOMAIN + settings.SUBPATH

    user = UserModel.objects.get(id=user_id)
    client = Client.objects.get(id=client_id)

    from_email = settings.EMAIL_FROM
    subject = f'您的账户已与{client.name}关联'
    tea_html = loader.render_to_string(
        'email/oidc_provider/consent_accept_alert.html',
        {
            'domain': domain,
            'name': user.get_full_name(),

            'client': client,
            'scopes': get_scopes_information(scope)
        }
    )
    my_send_mail.delay(subject, tea_html, from_email, [user.get_preferred_email()])
