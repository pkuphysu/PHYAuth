from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, gettext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.oidc_client.forms import FaqForm as OidcClientFaqForm
from app.oidc_client.models import Faq as OidcClientFaq
from app.utils.views import ErrorMessageMixin


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

    def get_object(self, queryset=None):
        pk = self.request.GET.get('pk')
        if pk is None:
            raise Http404(gettext('Please specify the pk!'))
        self.kwargs.update({'pk': self.request.GET.get('pk')})
        return super().get_object(queryset=queryset)

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
