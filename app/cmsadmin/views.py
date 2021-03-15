import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, Http404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from guardian.mixins import PermissionRequiredMixin as ObjectPermissionRequiredMixin, PermissionListMixin

from .forms import AnnouncementForm, TopLinkForm
from ..portal.models import Announcement, TopLink
from ..oidc_client.models import Faq as OidcClientFaq
from ..oidc_client.forms import FaqForm as OidcClientFaqForm
from ..utils.views import ErrorMessageMixin

User = get_user_model()
logger = logging.getLogger(__name__)


class AnnouncementListView(PermissionRequiredMixin, PermissionListMixin, ListView):
    model = Announcement
    permission_required = 'portal.view_announcement'
    template_name = 'cmsadmin/portal/announcement_list.html'
    permission_denied_message = _('You are not a staff, and do not have permission to view this page, '
                                  'please contact the administrator!')
    context_object_name = 'announcement_list'
    get_objects_for_user_extra_kwargs = {'accept_global_perms': False}


class AnnouncementCreateView(PermissionRequiredMixin, ObjectPermissionRequiredMixin,
                             SuccessMessageMixin, ErrorMessageMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'cmsadmin/portal/announcement_create.html'
    permission_object = None
    permission_required = 'portal.add_announcement'
    permission_denied_message = _('You are not a staff, and do not have permission to view this page, '
                                  'please contact the administrator!')
    error_message = _('Please check the error messages showed in the page!')

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'owner': self.request.user})
        return kwargs

    def get_success_message(self, cleaned_data):
        return _('Announcement #%(id)s has been created successfully!') % {'id': self.object.pk}

    def get_success_url(self):
        return reverse('cmsadmin:announcement-list')


class AnnouncementUpdateView(PermissionRequiredMixin, ObjectPermissionRequiredMixin,
                             SuccessMessageMixin, ErrorMessageMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'cmsadmin/portal/announcement_update.html'
    permission_required = 'portal.change_announcement'
    permission_denied_message = _('You are not the creator of this announcement, '
                                  'so you do not have the right to modify it!')
    error_message = _('Please check the error messages showed in the page!')

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'owner': self.request.user})
        return kwargs

    def get_success_message(self, cleaned_data):
        return _('Announcement #%(id)s has been updated successfully!') % {'id': self.object.pk}

    def get_success_url(self):
        return reverse('cmsadmin:announcement-list')


class AnnouncementDeleteView(PermissionRequiredMixin, ObjectPermissionRequiredMixin, DeleteView):
    model = Announcement
    permission_required = 'portal.delete_announcement'
    permission_denied_message = _('You are not the creator of this announcement, '
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


class TopLinkListView(PermissionRequiredMixin, PermissionListMixin, ListView):
    model = TopLink
    permission_required = 'portal.view_toplink'
    template_name = 'cmsadmin/portal/toplink_list.html'
    permission_denied_message = _('You are not a staff, and do not have permission to view this page, '
                                  'please contact the administrator!')
    context_object_name = 'toplink_list'
    get_objects_for_user_extra_kwargs = {'accept_global_perms': False}


class TopLinkCreateView(PermissionRequiredMixin, ObjectPermissionRequiredMixin,
                        SuccessMessageMixin, ErrorMessageMixin, CreateView):
    model = TopLink
    form_class = TopLinkForm
    template_name = 'cmsadmin/portal/toplink_create.html'
    permission_object = None
    permission_required = 'portal.add_toplink'
    permission_denied_message = _('You are not a staff, and do not have permission to view this page, '
                                  'please contact the administrator!')
    error_message = _('Please check the error messages showed in the page!')

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'owner': self.request.user})
        return kwargs

    def get_success_message(self, cleaned_data):
        return _('TopLink #%(id)s has been created successfully!') % {'id': self.object.pk}

    def get_success_url(self):
        return reverse('cmsadmin:toplink-list')


class TopLinkUpdateView(PermissionRequiredMixin, ObjectPermissionRequiredMixin,
                        SuccessMessageMixin, ErrorMessageMixin, UpdateView):
    model = TopLink
    form_class = TopLinkForm
    template_name = 'cmsadmin/portal/toplink_update.html'
    permission_required = 'portal.change_toplink'
    permission_denied_message = _('You are not the creator of this toplink, '
                                  'so you do not have the right to modify it!')
    error_message = _('Please check the error messages showed in the page!')

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'owner': self.request.user})
        return kwargs

    def get_success_message(self, cleaned_data):
        return _('Announcement #%(id)s has been updated successfully!') % {'id': self.object.pk}

    def get_success_url(self):
        return reverse('cmsadmin:toplink-list')


class TopLinkDeleteView(PermissionRequiredMixin, ObjectPermissionRequiredMixin, DeleteView):
    model = TopLink
    permission_required = 'portal.delete_toplink'
    permission_denied_message = _('You are not the creator of this toplink, '
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


class OidcClientFaqListView(PermissionRequiredMixin, ListView):
    model = OidcClientFaq
    permission_required = 'oidc_client.view_faq'
    permission_denied_message = _('You are not a staff, and do not have permission to view this page, '
                                  'please contact the administrator!')
    template_name = 'cmsadmin/oidc_client/faq_list.html'
    context_object_name = 'faq_list'


class OidcClientFaqCreateView(PermissionRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, CreateView):
    model = OidcClientFaq
    form_class = OidcClientFaqForm
    permission_required = 'oidc_client.add_faq'
    permission_denied_message = _('You are not a staff, and do not have permission to view this page, '
                                  'please contact the administrator!')
    error_message = _('Please check the error messages showed in the page!')
    template_name = 'cmsadmin/oidc_client/faq_create.html'

    def get_success_message(self, cleaned_data):
        return _('FAQ #%(id)s has been created successfully!') % {'id': self.object.pk}

    def get_success_url(self):
        return reverse('cmsadmin:oidc-client-faq-list')


class OidcClientFaqUpdateView(PermissionRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, UpdateView):
    model = OidcClientFaq
    form_class = OidcClientFaqForm
    permission_required = 'oidc_client.change_faq'
    permission_denied_message = _('You are not a staff, and do not have permission to view this page, '
                                  'please contact the administrator!')
    error_message = _('Please check the error messages showed in the page!')
    template_name = 'cmsadmin/oidc_client/faq_update.html'

    def get_success_message(self, cleaned_data):
        return _('FAQ #%(id)s has been updated successfully!') % {'id': self.object.pk}

    def get_success_url(self):
        return reverse('cmsadmin:oidc-client-faq-list')


class OidcClientFaqDeleteView(PermissionRequiredMixin, DeleteView):
    model = OidcClientFaq
    permission_required = 'oidc_client.delete_faq'
    permission_denied_message = _('You are not a staff, and do not have permission to delete this faq, '
                                  'please contact the administrator!')

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
