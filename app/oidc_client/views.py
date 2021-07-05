from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView, CreateView, ListView, DeleteView
from guardian.mixins import PermissionRequiredMixin as ObjectPermissionRequiredMixin, PermissionListMixin
from oidc_provider.models import Client

from .forms import ClientForm, AppGroupForm
from .models import Faq, AppGroup
from ..utils.views import ErrorMessageMixin


class FaqListView(ListView):
    model = Faq
    template_name = 'oidc_client/faq.html'
    context_object_name = 'faq_list'
    ordering = ('rank', 'id')

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(show=True)
        return qs


class ClientListView(PermissionRequiredMixin, PermissionListMixin, ListView):
    model = Client
    template_name = 'oidc_client/client_list.html'
    permission_required = 'oidc_provider.view_client'
    permission_denied_message = _('You are not a developer and do not have permission to view the application, '
                                  'please contact the administrator!')
    context_object_name = 'client_list'
    get_objects_for_user_extra_kwargs = {'with_superuser': False}
    ordering = 'pk'


class ClientCreateView(PermissionRequiredMixin, ObjectPermissionRequiredMixin,
                       SuccessMessageMixin, ErrorMessageMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'oidc_client/client_create.html'
    permission_object = None
    permission_required = 'oidc_provider.add_client'
    permission_denied_message = _('You are not a developer and do not have permission to view the application, '
                                  'please contact the administrator!')
    success_message = _('Client %(name)s has been created successfully!')
    error_message = _('Please check the error messages showed in the page!')

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('oidc_client:client-list')


class ClientUpdateView(PermissionRequiredMixin, ObjectPermissionRequiredMixin,
                       SuccessMessageMixin, ErrorMessageMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'oidc_client/client_update.html'
    permission_required = 'oidc_provider.change_client'
    permission_denied_message = _('You are not the creator of this application, '
                                  'so you do not have the right to modify this application!')
    success_message = _('Client %(name)s has been updated successfully!')
    error_message = _('Please check the error messages showed in the page!')
    return_403 = True

    def get_success_url(self):
        return reverse('oidc_client:client-list')


class AppGroupListView(PermissionRequiredMixin, PermissionListMixin, ListView):
    model = AppGroup
    template_name = 'oidc_client/appgroup_list.html'
    permission_required = 'oidc_client.view_appgroup'
    permission_denied_message = _('You are not a developer and do not have permission to view the app group, '
                                  'please contact the administrator!')
    context_object_name = 'appgroup_list'
    get_objects_for_user_extra_kwargs = {'with_superuser': False}
    ordering = 'pk'


class AppGroupCreateView(PermissionRequiredMixin, ObjectPermissionRequiredMixin,
                         SuccessMessageMixin, ErrorMessageMixin, CreateView):
    model = AppGroup
    form_class = AppGroupForm
    template_name = 'oidc_client/appgroup_create.html'
    permission_object = None
    permission_required = 'oidc_client.add_appgroup'
    permission_denied_message = _('You are not a developer and do not have permission to create app group, '
                                  'please contact the administrator!')
    success_message = _('App group %(name)s has been created successfully!')
    error_message = _('Please check the error messages showed in the page!')

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('oidc_client:appgroup-list')


class AppGroupUpdateView(PermissionRequiredMixin, ObjectPermissionRequiredMixin,
                         SuccessMessageMixin, ErrorMessageMixin, UpdateView):
    model = AppGroup
    form_class = AppGroupForm
    template_name = 'oidc_client/appgroup_update.html'
    permission_required = 'oidc_client.change_appgroup'
    permission_denied_message = _('You are not the creator of this app group, '
                                  'so you do not have the right to modify it!')
    success_message = _('App group %(name)s has been updated successfully!')
    error_message = _('Please check the error messages showed in the page!')
    return_403 = True

    def get_success_url(self):
        return reverse('oidc_client:appgroup-list')


class AppGroupDeleteView(PermissionRequiredMixin, DeleteView):
    model = AppGroup
    permission_required = 'oidc_client.delete_appgroup'
    permission_denied_message = _('You are not the creator of this app group, '
                                  'so you do not have the right to delete it!')

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.request.POST.get('id')
        if pk is None:
            raise Exception(_('Need %(verbose_name)s Id') % {'verbose_name': queryset.model._meta.verbose_name})
        queryset = queryset.filter(pk=pk)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse(data={'status': True})

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse(data={'status': False, 'msg': str(e)})
