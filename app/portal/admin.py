from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import TopLink, Announcement


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
        "title",
        "content",
        "rank"
    ]
