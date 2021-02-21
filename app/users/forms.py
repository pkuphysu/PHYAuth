import uuid

from django import forms
from django.contrib.auth.forms import UserCreationForm
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
            'first_name',
            'last_name',
            'email',
            'preferred_email',
            'nickname',
            'website',
            'gender',
            'birthdate',
            'phone_number',
            'address',
            'is_teacher',
            'in_school',
            'is_banned',
            'last_login',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['in_school'].disabled = True
        self.fields['is_teacher'].disabled = True
        self.fields['is_banned'].disabled = True
        self.fields['last_login'].disabled = True


class ClientForm(OIDC_ClientForm):
    class Meta(OIDC_ClientForm.Meta):
        model = Client
        exclude = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        print(self.user)
        super().__init__(*args, **kwargs)
        self.fields['owner'].required = False
        self.fields['owner'].initial = self.user
        self.fields['owner'].widget.attrs['disabled'] = 'true'
        self.fields['owner'].queryset = User.objects.filter(username=self.user.username)

    def clean_client_id(self):
        return str(uuid.uuid1())

    def clean_owner(self):
        return self.user
