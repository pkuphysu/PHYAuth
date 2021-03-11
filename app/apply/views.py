from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView, CreateView, ListView
from guardian.mixins import PermissionRequiredMixin as ObjectPermissionRequiredMixin, PermissionListMixin
from oidc_provider.models import Client

from .forms import ClientForm


class ClientListView(PermissionRequiredMixin, PermissionListMixin, ListView):
    model = Client
    template_name = 'apply/client_list.html'
    permission_required = 'oidc_provider.view_client'
    permission_denied_message = _('You are not a developer and do not have permission to view the application, '
                                  'please contact the administrator!')
    context_object_name = 'client_list'
    get_objects_for_user_extra_kwargs = {'with_superuser': False}


class ClientCreateView(PermissionRequiredMixin, ObjectPermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'apply/client_create.html'
    permission_object = None
    permission_required = 'oidc_provider.add_client'
    permission_denied_message = _('You are not a developer and do not have permission to view the application, '
                                  'please contact the administrator!')
    success_message = _('Client %(name)s has been created successfully!')

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('apply:client-list')


class ClientUpdateView(PermissionRequiredMixin, ObjectPermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'apply/client_update.html'
    permission_required = 'oidc_provider.change_client'
    permission_denied_message = _('You are not the creator of this application, '
                                  'so you do not have the right to modify this application!')
    success_message = _('Client %(name)s has been updated successfully!')
    return_403 = True

    def get_success_url(self):
        return reverse('apply:client-list')
