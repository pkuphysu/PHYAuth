from random import randint

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from oidc_provider.admin import ClientForm as OIDC_ClientForm
from oidc_provider.models import Client

from .models import Faq, AppGroup, MemberShip

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


class AppGroupForm(forms.ModelForm):
    class Meta:
        model = AppGroup
        fields = [
            'owner',
            'name',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'name': _('The name of your group.')
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['owner'].required = False
            self.fields['owner'].initial = self.user
            self.fields['owner'].queryset = UserModel.objects.filter(pk=self.user.pk)
        self.fields['owner'].disabled = True

    def clean_owner(self):
        return self.user


class MemberShipForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=UserModel.objects.all(),
                                  to_field_name='username',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  help_text=_('The pku id of the user which you are inviting.'),
                                  error_messages={
                                      'required': _('Please enter the user\'s pku id'),
                                      'invalid_choice': _('User of this pku id not found, maybe he/she have not'
                                                          'sign up with this site, please check again.')
                                  })

    field_order = ['user', 'remark', 'group', 'inviter']

    class Meta:
        model = MemberShip
        fields = [
            'group',
            'inviter',
            'user',
            'remark',
        ]
        widgets = {
            'group': forms.Select(attrs={'class': 'form-control'}),
            'inviter': forms.Select(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control',
                                            'rows': 3})
        }
        help_texts = {
            'remark': _('Some descriptions, e.g. invite reason.')
        }

    def __init__(self, *args, **kwargs):
        self.inviter = kwargs.pop('inviter', None)
        self.group = kwargs.pop('group', None)
        super().__init__(*args, **kwargs)
        if self.inviter:
            self.fields['inviter'].required = False
            self.fields['inviter'].initial = self.inviter
            self.fields['inviter'].queryset = UserModel.objects.filter(pk=self.inviter.pk)
        self.fields['inviter'].disabled = True
        if self.group:
            self.fields['group'].required = False
            self.fields['group'].initial = self.group
            self.fields['group'].queryset = AppGroup.objects.filter(pk=self.group.pk)
        self.fields['group'].disabled = True

    def clean_inviter(self):
        return self.inviter

    def clean_group(self):
        return self.group
