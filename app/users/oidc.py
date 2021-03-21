from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from oidc_provider.lib.claims import ScopeClaims

User = get_user_model()


def userinfo(claims, user: User):
    # Populate claims dict.
    claims['name'] = user.get_full_name()
    claims['given_name'] = user.first_name
    claims['family_name'] = user.last_name
    claims['nickname'] = user.nickname

    claims['website'] = user.website
    claims['gender'] = user.get_gender_display()
    claims['birthdate'] = user.birthdate

    claims['email'] = user.get_preferred_email()
    claims['email_verified'] = user.email

    claims['phone_number'] = user.phone_number

    claims['address']['formatted'] = user.address

    return claims


class CustomScopeClaims(ScopeClaims):
    info_profile = (
        _(u'Basic profile'),
        _(u'Access to your basic information. Includes names, given_name, family_name, nickname,'
          u' gender, birthdate and website.'),
    )

    info_email = (
        _(u'Email'),
        _(u'Access to your pku email address and preferred email address.'),
    )

    info_phone = (
        _(u'Phone number'),
        _(u'Access to your phone number.'),
    )

    info_address = (
        _(u'Address information'),
        _(u'Access to your address.'),
    )

    info_pku = (
        _(u'PKU Info'),
        _(u'Access to your pku information. Includes identity ID, '
          u'identity type, identity status, department, self introduce.'),
    )

    def scope_pku(self):
        # self.user - Django user instance.
        # self.userinfo - Dict returned by OIDC_USERINFO function.
        # self.scopes - List of scopes requested.
        # self.client - Client requesting this claims.
        dic = {
            'pku_id': self.user.username,
            'is_teacher': self.user.is_teacher,
            'in_school': self.user.in_school,
            'department': self.user.department.department,
            'introduce': self.user.introduce,
        }

        return dic


def check_profile(user):
    return user.get_full_name() and user.first_name and user.last_name \
           and user.nickname and user.website and user.birthdate


def check_email(user):
    return user.preferred_email and user.email


def check_phone(user):
    return user.phone_number


def check_address(user):
    return user.address


def check_pku(user):
    return user.department and user.introduce


def after_login_hook_func(request, user, client):
    scope = request.GET.get('scope', '').split()
    message = ''
    if ('profile' in scope and not check_profile(user)) or \
            ('email' in scope and not check_email(user)) or \
            ('phone' in scope and not check_phone(user)) or \
            ('address' in scope and not check_address(user)) or \
            ('pku' in scope and not check_pku(user)):
        message += _('Some of your information is not complete, '
                     'we recommend that you should complete your profile first.')

    if message:
        messages.add_message(request, messages.WARNING, message)
    return None
