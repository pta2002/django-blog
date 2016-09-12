from .models import Page

def pages(request):
    return {'sitepages': Page.objects.filter(show=True)}