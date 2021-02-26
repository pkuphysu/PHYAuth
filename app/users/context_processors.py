from .models import TopLink


def top_link(request):
    links = TopLink.objects.all().order_by('rank', 'id')

    return {'top_links': links}
