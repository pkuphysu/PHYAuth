from django.shortcuts import render

from .models import Announcement


def index(request):
    ctx = {
        'announcements': Announcement.objects.all().order_by('rank', '-id')
    }
    return render(request, 'index.html', context=ctx)
