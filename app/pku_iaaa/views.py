from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import View

from .models import Iaaa

UserModel = get_user_model()


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
        user = authenticate(request)

        if user is None:
            raise ValidationError(_("No account is found."))
        elif user.is_banned is True:
            raise ValidationError(_("Your account was banned by admin, please contact the Student "
                                    "Affairs Office of the School of Physics for help."))
        elif user.is_active is False:
            raise ValidationError(_("This application temporarily only serves the teachers and students of the School "
                                    "of Physics. Your personal relationship is not in the School of Physics. "
                                    "Therefore, temporarily mark your account as disabled. Please contact the Student "
                                    "Affairs Office of the School of Physics to activate your account."))
        else:
            login(request, user)

        if request.COOKIES.get('next'):
            redirect_to = request.COOKIES.get('next')
            response = HttpResponseRedirect(redirect_to)
            sub_path = request.META.get("SCRIPT_NAME") if request.META.get("SCRIPT_NAME") != '' else '/'
            response.delete_cookie('next', path=sub_path)
            return response
        return HttpResponseRedirect(reverse('index'))
