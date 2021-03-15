from django.contrib.auth import get_user_model
from django.db.models import Q
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
        'admins': User.objects.filter(Q(is_admin=True) | Q(is_superuser=True))
    }
    return render(request, 'portal/admins.html', context=ctx)
