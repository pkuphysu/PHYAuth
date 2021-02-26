from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView, CreateView, ListView
from oidc_provider.models import UserConsent, Client

from .forms import UserForm, ClientForm
from .models import Announcement

UserModel = get_user_model()


def index(request):
    ctx = {
        'announcements': Announcement.objects.all().order_by('rank', '-id')
    }
    return render(request, 'index.html', context=ctx)


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/user_detail.html'
    form_class = UserForm

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


class ClientListView(PermissionRequiredMixin, ListView):
    template_name = 'users/client_list.html'
    permission_required = 'oidc_provider.view_client'
    permission_denied_message = '您不是开发者，无权查看应用，请联系管理员！'
    context_object_name = 'client_list'

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientCreateView(PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'users/client_create.html'
    permission_required = 'oidc_provider.add_client'
    permission_denied_message = '您不是开发者，无权申请应用，请联系管理员！'

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('users:client-list')


class ClientUpdateView(PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'users/client_update.html'
    permission_required = 'oidc_provider.change_client'
    permission_denied_message = '您不是开发者，无权申请应用，请联系管理员！'

    def get_success_url(self):
        return reverse('users:client-list')
