from django.utils.translation import ugettext as _
from oidc_provider.lib.claims import ScopeClaims
from django.contrib.auth import get_user_model

User = get_user_model()


def userinfo(claims, user: User):
    # Populate claims dict.
    claims['name'] = '{}{}'.format(user.last_name, user.first_name)
    claims['given_name'] = user.first_name
    claims['family_name'] = user.last_name
    claims['nickname'] = user.nickname

    claims['website'] = user.website
    claims['gender'] = user.gender
    claims['birthdate'] = user.birthdate

    claims['email'] = user.email

    claims['phone_number'] = user.phone_number

    claims['address']['formatted'] = user.address

    return claims


class CustomScopeClaims(ScopeClaims):
    info_extra = (
        _(u'Extra'),
        _(u'Extra information.'),
    )

    def scope_extra(self):
        # self.user - Django user instance.
        # self.userinfo - Dict returned by OIDC_USERINFO function.
        # self.scopes - List of scopes requested.
        # self.client - Client requesting this claims.
        dic = {
            'id': self.user.username,
            'preferred_email': self.user.get_preferred_email(),
            'is_teacher': self.user.is_teacher,
            'in_school': self.user.in_school,
            'is_banned': self.user.is_banned,
        }

        return dic
