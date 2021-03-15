import hashlib
import logging

import requests
from django.contrib.auth import get_user_model
from django.core.exceptions import SuspiciousOperation

from .models import Iaaa
from .signals import iaaa_user_create

UserModel = get_user_model()
logger = logging.getLogger(__name__)


class IaaaError(Exception):
    """Error returned by PKU IAAA Server"""

    def __init__(self, code, msg, *args, **kwargs):
        response = kwargs.pop("response", None)
        self.response = response
        msg = "[%s] %s" % (
            code, msg
        )
        super(IaaaError, self).__init__(msg)


class IaaaAuthenticationBackend:
    # Create a User object if not already in the database?
    create_unknown_user = True

    def authenticate(self, request, _rand=None, token=None):
        if token is None:
            raise SuspiciousOperation

        if request.META.get('HTTP_X_FORWARDED_FOR'):
            remote_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        else:
            remote_ip = request.META.get('REMOTE_ADDR')

        user_info = self.iaaa_auth(rand=_rand, token=token, remote_ip=remote_ip)
        logger.debug(user_info)
        identity_id = user_info["identityId"]

        user = None
        if self.create_unknown_user:
            user, created = UserModel._default_manager.get_or_create(**{
                UserModel.USERNAME_FIELD: identity_id
            })
            if created:
                user = self.configure_user(user_info, user)
                logger.info(self.__class__.__name__ + f' create a user {user.id}')
                iaaa_user_create.send(sender=self.__class__, user_id=user.id)
        else:
            try:
                user = UserModel._default_manager.get_by_natural_key(identity_id)
            except UserModel.DoesNotExist:
                pass
        return user

    @classmethod
    def configure_user(cls, user_info, user):
        """
        Configure a user after creation and return the updated user.

        By default, return the user unmodified.
        """
        if user_info['deptId'] != '00004':
            user.is_active = False

        user.is_teacher = False if user_info['identityType'] == '学生' else True
        if user.is_teacher:
            user.in_school = True if user_info['detailType'] == '在职' else False
        else:
            user.in_school = True if user_info['identityStatus'] == '在校' else False
        user.email = user.get_pku_email()
        user.name = user_info['name']
        user.nickname = user_info['name']
        user.save()
        return user

    @classmethod
    def iaaa_auth(cls, rand, token, remote_ip):

        app = Iaaa.objects.last()
        app_id = app.app_id
        key = app.key

        para_str = "appId=%s&remoteAddr=%s&token=%s" % (app_id, remote_ip, token) + key

        msg_abs = hashlib.md5()
        msg_abs.update(para_str.encode('utf-8'))

        url = "https://iaaa.pku.edu.cn/iaaa/svc/token/validate.do?remoteAddr=%s&appId=%s&token=%s&msgAbs=%s" % \
              (remote_ip, app_id, token, msg_abs.hexdigest())

        try:
            iaaa_response = requests.get(url=url)
        except requests.exceptions.RequestException as e:
            raise e
        try:
            response = iaaa_response.json()
        except ValueError as e:
            raise e
        if response['success']:
            user_info = response['userInfo']
            return user_info
        else:
            raise IaaaError(response["errCode"], response["errMsg"])

    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user
