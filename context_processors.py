from .models import MenuLink

# DEPRECATED
def pages(request):
    return {'sitepages': MenuLink.objects.all().order_by('order')}

def links(request):
    return {'menulinks': MenuLink.objects.all().order_by('order')}