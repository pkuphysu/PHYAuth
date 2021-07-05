from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core import signing
from django.core.signing import SignatureExpired, BadSignature
from django.db import IntegrityError
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import UpdateView, CreateView, ListView, DeleteView
from guardian.mixins import PermissionRequiredMixin as ObjectPermissionRequiredMixin, PermissionListMixin
from oidc_provider.models import Client

from .forms import ClientForm, AppGroupForm, MemberShipForm
from .models import Faq, AppGroup, MemberShip
from ..users.models import User
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


class AppGroupDeleteView(PermissionRequiredMixin, ObjectPermissionRequiredMixin, DeleteView):
    model = AppGroup
    permission_required = 'oidc_client.delete_appgroup'
    permission_denied_message = _('You are not the creator of this app group, '
                                  'so you do not have the right to delete it!')

    def on_permission_check_fail(self, request, response, obj=None):
        raise PermissionDenied(_('You are not the creator of this app group, '
                                 'so you do not have the right to delete it!'))

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


class AppGroupUserListView(PermissionRequiredMixin, ObjectPermissionRequiredMixin, ListView):
    model = MemberShip
    template_name = 'oidc_client/appgroup_user_list.html'
    permission_required = 'oidc_client.view_appgroup'
    permission_denied_message = _('You are not a developer and do not have permission to view the user of this group, '
                                  'please contact the administrator!')
    context_object_name = 'membership_list'
    ordering = 'date_joined'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['group'] = self.get_object()
        return ctx

    def get_object(self):
        return AppGroup.objects.get(id=self.kwargs.get('gid'))

    def get_queryset(self):
        return super().get_queryset().filter(group__id=self.kwargs.get('gid'))


class AppGroupInviteUserView(PermissionRequiredMixin, ObjectPermissionRequiredMixin,
                             SuccessMessageMixin, ErrorMessageMixin, CreateView):
    model = MemberShip
    form_class = MemberShipForm
    template_name = 'oidc_client/appgroup_user_invite.html'
    permission_required = 'oidc_client.change_appgroup'
    permission_denied_message = _('You are not a developer or the owner of this group, '
                                  'so you do not have permission to invite user!')
    success_message = _('Successfully invite %(name)s!')
    error_message = _('Please check the error messages showed in the page!')

    def get_success_message(self, cleaned_data):
        user = User.objects.get(username=cleaned_data['user'])
        return self.success_message % {'name': user.name}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['group'] = self.permission_object
        return ctx

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            self.error_message = _('This user has been invited before, Use the reinvite button!')
            return super().form_invalid(form)

    @property
    def permission_object(self):
        return AppGroup.objects.get(id=self.kwargs.get('gid'))

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'inviter': self.request.user})
        kwargs.update({'group': self.permission_object})
        return kwargs

    def get_success_url(self):
        return reverse('oidc_client:appgroup-user', kwargs={'gid': self.kwargs.get('gid')})


class AppGroupInviteUserAcceptView(View):
    def get(self, request, gid, signstr):
        try:
            value = signing.loads(signstr, max_age=timedelta(weeks=1))
            ms_id = value['ms_id']
            ms = MemberShip.objects.get(id=ms_id)
            ms.date_joined = timezone.now()
            ms.save()
            messages.success(request, message=_("Success join the %(group_name)s") % {'group_name': ms.group.name})
        except SignatureExpired:
            messages.error(request,
                           message=_("Signature had expired, please contact the app admin to resend invitation."))
        except BadSignature:
            messages.error(request, message=_('url invalid, please check again!'))
        return redirect(reverse('users:user-profile'))


class AppGroupDelUserView(PermissionRequiredMixin, ObjectPermissionRequiredMixin, DeleteView):
    model = MemberShip
    permission_required = 'oidc_client.change_appgroup'
    permission_denied_message = _('You are not the creator of this app group, '
                                  'so you do not have the right to delete its user!')

    def on_permission_check_fail(self, request, response, obj=None):
        raise PermissionDenied(_('You are not the creator of this app group, '
                                 'so you do not have the right to delete its user!'))

    @property
    def permission_object(self):
        return AppGroup.objects.get(id=self.kwargs.get('gid'))

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
