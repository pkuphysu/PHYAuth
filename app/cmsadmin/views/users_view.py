from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, gettext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.users.forms import UserForm as IUserForm
from app.users.models import User
from app.utils.views import ErrorMessageMixin


class UserForm(IUserForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = False
        self.fields['in_school'].disabled = False
        self.fields['is_teacher'].disabled = False
        self.fields['is_admin'].disabled = False


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_user'
    permission_denied_message = _('You are not a staff, and do not have permission to view this page, '
                                  'please contact the administrator!')
    template_name = 'cmsadmin/users/user_list.html'
    context_object_name = 'user_list'
    paginate_by = 50


class UserCreateView(PermissionRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, CreateView):
    model = User
    form_class = UserForm
    permission_required = 'users.add_user'
    permission_denied_message = _('You are not a staff, and do not have permission to view this page, '
                                  'please contact the administrator!')
    error_message = _('Please check the error messages showed in the page!')
    template_name = 'cmsadmin/users/user_create.html'

    def get_success_message(self, cleaned_data):
        return _('User #%(id)s has been created successfully!') % {'id': self.object.username}

    def get_success_url(self):
        return reverse('cmsadmin:users-user-list')


class UserUpdateView(PermissionRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    permission_required = 'users.change_user'
    permission_denied_message = _('You are not a staff, and do not have permission to view this page, '
                                  'please contact the administrator!')
    error_message = _('Please check the error messages showed in the page!')
    template_name = 'cmsadmin/users/user_update.html'

    def get_object(self, queryset=None):
        pk = self.request.GET.get('pk')
        if pk is None:
            raise Http404(gettext('Please specify the pk!'))
        self.kwargs.update({'pk': self.request.GET.get('pk')})
        return super().get_object(queryset=queryset)

    def get_success_message(self, cleaned_data):
        return _('User #%(id)s has been updated successfully!') % {'id': self.object.username}

    def get_success_url(self):
        return reverse('cmsadmin:users-user-list')


class UserDeleteView(PermissionRequiredMixin, DeleteView):
    model = User
    permission_required = 'users.delete_user'
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
