from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import signing
from django.template import loader
from django.urls import reverse
from oidc_provider.models import Client

from PHYAuth.celery import TransactionAwareTask, my_send_mail
from .models import ClientUserMemberShip
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


@shared_task(base=TransactionAwareTask)
def clientgroup_invite_user_email(ms_id):
    domain = settings.DOMAIN + settings.SUBPATH

    ms = ClientUserMemberShip.objects.get(id=ms_id)
    group = ms.group
    user = ms.user
    inviter = ms.inviter

    if domain.endswith('/'):
        invite_url = domain[:-1]
    else:
        invite_url = domain

    value = signing.dumps({'ms_id': ms.id})

    invite_url += reverse('oidc_client:clientgroup-user-invite-accept', kwargs={'gid': group.id, 'signstr': value})

    from_email = settings.EMAIL_FROM
    subject = f'{inviter.name}邀请您加入{group.name}'
    tea_html = loader.render_to_string(
        'email/oidc_provider/clientgroup_invite_user.html',
        {
            'domain': domain,
            'name': user.get_full_name(),
            'group': group,
            'inviter': inviter,
            'invite_url': invite_url,
        }
    )
    my_send_mail.delay(subject, tea_html, from_email, [user.get_preferred_email()])
