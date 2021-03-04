import logging

from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import HttpResponseRedirect, Http404
from django.template.response import TemplateResponse
from django.urls import reverse
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
        app = Iaaa.objects.get(pk=1)
        ctx = {
            'app_id': app.app_id,
            'redirect_url': app.redirect_url,
            'local_login_redirect_url': request.build_absolute_uri(reverse('login'))
        }
        response = TemplateResponse(request, template='pku_iaaa/login.html', context=ctx)

        redirect_to = request.POST.get('next', request.GET.get('next', ''))
        if redirect_to:
            sub_path = request.META.get("SCRIPT_NAME") if request.META.get("SCRIPT_NAME") != '' else '/'
            response.set_cookie(key='next', value=redirect_to, expires=5 * 60, path=sub_path)
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

        if request.COOKIES.get('next'):
            redirect_to = request.COOKIES.get('next')
            response = HttpResponseRedirect(redirect_to)
            sub_path = request.META.get("SCRIPT_NAME") if request.META.get("SCRIPT_NAME") != '' else '/'
            response.delete_cookie('next', path=sub_path)
            return response
        return HttpResponseRedirect(reverse('index'))
