from django import forms
from django.contrib.auth.forms import UserCreationForm

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
            'is_admin',
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
            'is_admin': forms.Select(attrs={'class': 'form-control'}),
            'last_login': forms.DateTimeInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['in_school'].disabled = True
        self.fields['is_teacher'].disabled = True
        self.fields['is_admin'].disabled = True
        self.fields['last_login'].disabled = True
