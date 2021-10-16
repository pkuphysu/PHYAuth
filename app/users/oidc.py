from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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
    # TODO: email_verified should be true or false, not another email address...
    # claims['email_verified'] = user.email

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
          u'identity type, identity status, department, self introduce, and groups.'),
    )

    def scope_pku(self):
        # self.user - Django user instance.
        # self.userinfo - Dict returned by OIDC_USERINFO function.
        # self.scopes - List of scopes requested.
        # self.client - Client requesting this claims.
        try:
            self.user.username_validator(self.user.username)
            is_pku = True
        except ValidationError:
            is_pku = False
        dic = {
            'is_pku': is_pku,
            'pku_id': self.user.username,
            'pku_email': self.user.email,
            'is_teacher': self.user.is_teacher,
            'in_school': self.user.in_school,
            'department': self.user.department.department if self.user.department else None,
            'introduce': self.user.introduce,
            'groups': list(self.user.clientusermembership_set.filter(
                group__client=self.client, date_joined__isnull=False).values_list('group__name', flat=True))
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
