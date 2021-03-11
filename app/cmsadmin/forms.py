from django import forms
from django.contrib.auth import get_user_model

from ..portal.models import Announcement, TopLink

User = get_user_model()


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            'owner',
            'type',
            'title',
            'content',
            'rank'
        ]
        widgets = {
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'rank': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['owner'].initial = self.user
            self.fields['owner'].queryset = User.objects.filter(username=self.user.username)
        self.fields['owner'].disabled = True

    def clean_owner(self):
        return self.user


class TopLinkForm(forms.ModelForm):
    class Meta:
        model = TopLink
        fields = [
            'owner',
            'rank',
            'name',
            'url',
        ]
        widgets = {
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'rank': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['owner'].initial = self.user
            self.fields['owner'].queryset = User.objects.filter(username=self.user.username)
        self.fields['owner'].disabled = True

    def clean_owner(self):
        return self.user
