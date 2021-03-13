import logging

from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import HttpResponseRedirect, Http404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext, gettext_lazy as _
from django.views.generic.base import View

from .auth_backends import IaaaAuthenticationBackend
from .models import Iaaa
from .signals import iaaa_user_login_success

UserModel = get_user_model()
backend = IaaaAuthenticationBackend()
logger = logging.getLogger(__name__)


class IAAALoginView(View):
    def get(self, request):
        app = Iaaa.objects.last()
        redirect_to = request.POST.get(
            REDIRECT_FIELD_NAME,
            request.GET.get(REDIRECT_FIELD_NAME, '')
        )

        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        )
        redirect_to = redirect_to if url_is_safe else ''

        if redirect_to:
            request.session[REDIRECT_FIELD_NAME] = redirect_to

        ctx = {
            'app_id': app.app_id,
            'redirect_url': app.redirect_url,
        }
        response = TemplateResponse(request, template='pku_iaaa/login.html', context=ctx)
        return response


class IAAALoginAuth(View):
    def get(self, request):
        _rand = request.GET.get('_rand')
        token = request.GET.get('token')
        if token is None:
            logger.error('Token argument not provided.')
            raise SuspiciousOperation

        try:
            user = backend.authenticate(request, _rand=_rand, token=token)
        except Exception as e:
            msg = e.__class__.__name__
            try:
                message = e.args[0]
            except (AttributeError, IndexError):
                pass
            else:
                if isinstance(message, str):
                    msg = message
            logger.exception(msg)
            raise Http404(msg)
        if user is None:
            raise Http404(gettext("No account is found."))
        elif user.is_active is False:
            raise PermissionDenied(_("This application temporarily only serves the teachers and students of the School "
                                     "of Physics. Now your personal relationship is not in the School of Physics "
                                     "or your account is disabled. Please contact the Student "
                                     "Affairs Office of the School of Physics to activate your account."))
        else:
            backend_path = backend.__module__ + '.' + backend.__class__.__name__
            user.backend = backend_path
            login(request, user)
            logger.info(f'user {user.username} login by iaaa auth')
            iaaa_user_login_success.send(sender=self.__class__, user_id=user.id)

        if request.session.get(REDIRECT_FIELD_NAME, ''):
            redirect_to = request.session.get(REDIRECT_FIELD_NAME)
            logger.info(redirect_to)
            del request.session[REDIRECT_FIELD_NAME]
            return HttpResponseRedirect(redirect_to=redirect_to)

        return HttpResponseRedirect(reverse('index'))
