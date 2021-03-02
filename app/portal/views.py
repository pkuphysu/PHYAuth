from django.contrib.auth import get_user_model
from django.shortcuts import render

from .models import Announcement

User = get_user_model()


def index(request):
    ctx = {
        'announcements': Announcement.objects.all().order_by('rank', '-id')
    }
    return render(request, 'index.html', context=ctx)


def admins(request):
    ctx = {
        'admins': User.objects.filter(is_staff=True)
    }
    return render(request, 'portal/admins.html', context=ctx)
