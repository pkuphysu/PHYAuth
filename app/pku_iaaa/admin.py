from django.contrib import admin

from .models import Iaaa


@admin.register(Iaaa)
class IaaaAdmin(admin.ModelAdmin):
    list_display = [
        "app_id",
        "key",
        "redirect_url"
    ]
