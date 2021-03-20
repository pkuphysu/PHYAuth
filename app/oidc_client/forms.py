from random import randint

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from oidc_provider.admin import ClientForm as OIDC_ClientForm
from oidc_provider.models import Client

from .models import Faq

UserModel = get_user_model()


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
            self.fields['owner'].queryset = UserModel.objects.filter(pk=self.user.pk)
        self.fields['owner'].disabled = True

        self.fields['website_url'].required = True
        self.fields['require_consent'].disabled = True

    def clean_client_id(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.client_id
        else:
            import time
            return str(int(time.time())) + str(randint(1, 999)).zfill(4)

    def clean_owner(self):
        return self.user


class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = [
            'question',
            'answer',
            'show',
            'rank'
        ]
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control summernote'}),
            'show': forms.Select(attrs={'class': 'form-control'}),
            'rank': forms.NumberInput(attrs={'class': 'form-control'}),
        }
