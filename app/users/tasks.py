from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template import loader
from oidc_provider import settings as oidc_settings
from oidc_provider.lib.claims import StandardScopeClaims
from oidc_provider.models import Client

from PHYAuth.celery import TransactionAwareTask, my_send_mail

UserModel = get_user_model()


def get_scopes_information(scope_o):
    """
    Return a list with the description of all the scopes requested.
    """
    scopes = StandardScopeClaims.get_scopes_info(scope_o)
    if oidc_settings.get('OIDC_EXTRA_SCOPE_CLAIMS'):
        scopes_extra = oidc_settings.get(
            'OIDC_EXTRA_SCOPE_CLAIMS', import_str=True).get_scopes_info(scope_o)
        for index_extra, scope_extra in enumerate(scopes_extra):
            for index, scope in enumerate(scopes[:]):
                if scope_extra['scope'] == scope['scope']:
                    del scopes[index]
    else:
        scopes_extra = []

    return scopes + scopes_extra


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
            'name': user.get_full_name(),
        }
    )
    my_send_mail.delay(subject, tea_html, from_email, [user.get_preferred_email()])
