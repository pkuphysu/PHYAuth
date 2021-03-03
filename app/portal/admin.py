from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import TopLink, Announcement


@admin.register(TopLink)
class TopLinkAdmin(GuardedModelAdmin):
    list_display = [
        "name",
        "url",
        "rank"
    ]


@admin.register(Announcement)
class AnnouncementAdmin(GuardedModelAdmin):
    list_display = [
        "type",
        "title",
        "content",
        "rank"
    ]
