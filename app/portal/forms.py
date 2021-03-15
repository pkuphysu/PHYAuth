from django import forms
from django.contrib.auth import get_user_model

from .models import Announcement, TopLink

User = get_user_model()


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            'type',
            'title',
            'content',
            'rank'
        ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'rank': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class TopLinkForm(forms.ModelForm):
    class Meta:
        model = TopLink
        fields = [
            'rank',
            'name',
            'url',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'rank': forms.NumberInput(attrs={'class': 'form-control'}),
        }
