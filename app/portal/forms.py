from django import forms

from .models import Announcement, TopLink


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            'title',
            'content',
            'rank'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control summernote'}),
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
