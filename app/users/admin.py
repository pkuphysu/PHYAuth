from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, TopLink, Announcement


class UserAdmin(AbstractUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': (
            'first_name', 'last_name', 'nickname', 'email', 'preferred_email', 'gender',
            'birthdate', 'phone_number', 'address', 'website'
        )}),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Account Status'), {'fields': ('is_active', 'is_teacher', 'in_school')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )

    def get_name(self, obj):
        return '{}{}'.format(obj.last_name, obj.first_name)

    get_name.short_description = _('Full Name')

    list_display = ('username', 'get_name', 'nickname', 'email', 'is_teacher', 'in_school')
    list_filter = ('is_teacher', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'nickname')


admin.site.register(User, UserAdmin)


@admin.register(TopLink)
class TopLinkAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "url",
        "rank"
    ]


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        "type",
        "title",
        "content",
        "rank"
    ]
