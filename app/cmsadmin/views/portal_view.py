from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, gettext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.portal.forms import AnnouncementForm, TopLinkForm
from app.portal.models import Announcement, TopLink
from app.utils.views import ErrorMessageMixin


class AnnouncementListView(PermissionRequiredMixin, ListView):
    model = Announcement
    permission_required = 'portal.view_announcement'
    template_name = 'cmsadmin/portal/announcement_list.html'
    permission_denied_message = _('You are not a staff, and do not have permission to view this page, '
                                  'please contact the administrator!')
    context_object_name = 'announcement_list'


class AnnouncementCreateView(PermissionRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'cmsadmin/portal/announcement_create.html'
    permission_required = 'portal.add_announcement'
    permission_denied_message = _('You are not a staff, and do not have permission to view this page, '
                                  'please contact the administrator!')
    error_message = _('Please check the error messages showed in the page!')

    def get_success_message(self, cleaned_data):
        return _('Announcement #%(id)s has been created successfully!') % {'id': self.object.pk}

    def get_success_url(self):
        return reverse('cmsadmin:portal-announcement-list')


class AnnouncementUpdateView(PermissionRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'cmsadmin/portal/announcement_update.html'
    permission_required = 'portal.change_announcement'
    permission_denied_message = _('You are not the creator of this announcement, '
                                  'so you do not have the right to modify it!')
    error_message = _('Please check the error messages showed in the page!')

    def get_object(self, queryset=None):
        pk = self.request.GET.get('pk')
        if pk is None:
            raise Http404(gettext('Please specify the pk!'))
        self.kwargs.update({'pk': self.request.GET.get('pk')})
        return super().get_object(queryset=queryset)

    def get_success_message(self, cleaned_data):
        return _('Announcement #%(id)s has been updated successfully!') % {'id': self.object.pk}

    def get_success_url(self):
        return reverse('cmsadmin:portal-announcement-list')


class AnnouncementDeleteView(PermissionRequiredMixin, DeleteView):
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


class TopLinkListView(PermissionRequiredMixin, ListView):
    model = TopLink
    permission_required = 'portal.view_toplink'
    template_name = 'cmsadmin/portal/toplink_list.html'
    permission_denied_message = _('You are not a staff, and do not have permission to view this page, '
                                  'please contact the administrator!')
    context_object_name = 'toplink_list'


class TopLinkCreateView(PermissionRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, CreateView):
    model = TopLink
    form_class = TopLinkForm
    template_name = 'cmsadmin/portal/toplink_create.html'
    permission_required = 'portal.add_toplink'
    permission_denied_message = _('You are not a staff, and do not have permission to view this page, '
                                  'please contact the administrator!')
    error_message = _('Please check the error messages showed in the page!')

    def get_success_message(self, cleaned_data):
        return _('TopLink #%(id)s has been created successfully!') % {'id': self.object.pk}

    def get_success_url(self):
        return reverse('cmsadmin:portal-toplink-list')


class TopLinkUpdateView(PermissionRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, UpdateView):
    model = TopLink
    form_class = TopLinkForm
    template_name = 'cmsadmin/portal/toplink_update.html'
    permission_required = 'portal.change_toplink'
    permission_denied_message = _('You are not the creator of this toplink, '
                                  'so you do not have the right to modify it!')
    error_message = _('Please check the error messages showed in the page!')

    def get_object(self, queryset=None):
        pk = self.request.GET.get('pk')
        if pk is None:
            raise Http404(gettext('Please specify the pk!'))
        self.kwargs.update({'pk': self.request.GET.get('pk')})
        return super().get_object(queryset=queryset)

    def get_success_message(self, cleaned_data):
        return _('Announcement #%(id)s has been updated successfully!') % {'id': self.object.pk}

    def get_success_url(self):
        return reverse('cmsadmin:portal-toplink-list')


class TopLinkDeleteView(PermissionRequiredMixin, DeleteView):
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
