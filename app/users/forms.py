from django.contrib.auth.forms import UserCreationForm
from django import forms
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

        # widgets = {
        #     # 'username': forms.TextInput(attrs={'disabled': True}),
        #     'is_teacher': forms.Select(attrs={'disabled': True}),
        #     'in_school': forms.Select(attrs={'disabled': True}),
        #     'is_banned': forms.Select(attrs={'disabled': True}),
        #     'last_login': forms.TextInput(attrs={'disabled': True}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['in_school'].disabled = True
        self.fields['is_teacher'].disabled = True
        self.fields['is_banned'].disabled = True
        self.fields['last_login'].disabled = True
