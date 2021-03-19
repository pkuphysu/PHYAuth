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
