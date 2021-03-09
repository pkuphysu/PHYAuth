import uuid

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from oidc_provider.admin import ClientForm as OIDC_ClientForm
from oidc_provider.models import Client

from .models import User


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'first_name',
            'last_name',
            'email',
            'preferred_email',
            'nickname',
            'department',
            'website',
            'gender',
            'birthdate',
            'phone_number',
            'address',
            'introduce',
            'is_teacher',
            'in_school',
            'last_login',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'preferred_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'introduce': forms.Textarea(attrs={'class': 'form-control',
                                               'rows': 3}),
            'is_teacher': forms.Select(attrs={'class': 'form-control'}),
            'in_school': forms.Select(attrs={'class': 'form-control'}),
            'last_login': forms.DateTimeInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['in_school'].disabled = True
        self.fields['is_teacher'].disabled = True
        self.fields['last_login'].disabled = True


class ClientForm(OIDC_ClientForm):
    class Meta(OIDC_ClientForm.Meta):
        model = Client
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'client_type': forms.Select(attrs={'class': 'form-control'}),
            'client_id': forms.TextInput(attrs={'class': 'form-control'}),
            'client_secret': forms.TextInput(attrs={'class': 'form-control'}),
            'response_types': forms.SelectMultiple(attrs={'class': 'form-control'}),
            '_scope': forms.TextInput(attrs={'class': 'form-control',
                                             'rows': 1}),
            'jwt_alg': forms.Select(attrs={'class': 'form-control'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control'}),
            'terms_url': forms.URLInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'custom-file-input'}),
            'reuse_consent': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'require_consent': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            '_redirect_uris': forms.Textarea(attrs={'class': 'form-control',
                                                    'rows': 3}),
            '_post_logout_redirect_uris': forms.Textarea(attrs={'class': 'form-control',
                                                                'rows': 3})
        }
        help_texts = {
            'client_id': _('Client ID will be generated randomly.'),
            'client_secret': _('Client Secret will be generated randomly. '
                               'If you want to get a new secret, please switch '
                               'the client to Public and save, then switch back and save.')
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['owner'].required = False
            self.fields['owner'].initial = self.user
            self.fields['owner'].queryset = User.objects.filter(username=self.user.username)
        self.fields['owner'].disabled = True

        self.fields['website_url'].required = True
        self.fields['require_consent'].disabled = True

    def clean_client_id(self):
        return str(uuid.uuid1())

    def clean_owner(self):
        return self.user
