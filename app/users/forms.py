from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User, Department


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
            'last_iaaa_login',
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
            'birthdate': forms.DateInput(attrs={'class': 'form-control datetimepicker-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'introduce': forms.Textarea(attrs={'class': 'form-control',
                                               'rows': 3}),
            'is_teacher': forms.Select(attrs={'class': 'form-control'}),
            'in_school': forms.Select(attrs={'class': 'form-control'}),
            'is_admin': forms.Select(attrs={'class': 'form-control'}),
            'last_iaaa_login': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'last_login': forms.DateTimeInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['in_school'].disabled = True
        self.fields['is_teacher'].disabled = True
        self.fields['is_admin'].disabled = True
        self.fields['last_iaaa_login'].disabled = True
        self.fields['last_login'].disabled = True


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            'department'
        ]
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control'})
        }


class MyAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
        'need_iaaa': _("You need use iaaa for login to update your account state. "
                       "This request will appear every three months."),
    }

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        super().confirm_login_allowed(user)
        from django.utils import timezone
        from datetime import timedelta
        # 非本校人士无需校验 IAAA 登录
        try:
            user.username_validator(user.username)
        except ValidationError:
            return
        if user.last_iaaa_login is None or timezone.now() - user.last_iaaa_login > timedelta(weeks=12):
            raise ValidationError(
                self.error_messages['need_iaaa'],
                code='need_iaaa',
            )

