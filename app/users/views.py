from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView, CreateView, ListView
from guardian.mixins import PermissionRequiredMixin as ObjectPermissionRequiredMixin, PermissionListMixin
from oidc_provider.models import UserConsent, Client

from .forms import UserForm, ClientForm

UserModel = get_user_model()


class UserProfileView(ObjectPermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'users/user_detail.html'
    form_class = UserForm
    permission_required = ['users.change_user', 'users.view_user']
    raise_exception = True
    success_message = _('Your profile has been updated successfully!')

    def get_context_data(self, **kwargs):
        ctx = super(UserProfileView, self).get_context_data(**kwargs)
        user = self.get_object()
        consents = UserConsent.objects.filter(user=user).order_by('-id')
        ctx.update({'consents': consents})
        return ctx

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('users:user-profile')


class ClientListView(PermissionRequiredMixin, PermissionListMixin, ListView):
    model = Client
    template_name = 'users/client_list.html'
    permission_required = 'oidc_provider.view_client'
    raise_exception = True
    permission_denied_message = _('You are not a developer and do not have permission to view the application, '
                                  'please contact the administrator!')
    context_object_name = 'client_list'
    get_objects_for_user_extra_kwargs = {'with_superuser': False}


class ClientCreateView(PermissionRequiredMixin, ObjectPermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'users/client_create.html'
    permission_object = None
    permission_required = 'oidc_provider.add_client'
    raise_exception = True
    permission_denied_message = _('You are not a developer and do not have permission to view the application, '
                                  'please contact the administrator!')
    success_message = _('Client %(name)s has been created successfully!')

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('users:client-list')


class ClientUpdateView(PermissionRequiredMixin, ObjectPermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'users/client_update.html'
    permission_required = 'oidc_provider.change_client'
    permission_denied_message = _('You are not the creator of this application, '
                                  'so you do not have the right to modify this application!')
    raise_exception = True
    success_message = _('Client %(name)s has been updated successfully!')

    def get_success_url(self):
        return reverse('users:client-list')
