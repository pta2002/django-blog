from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<permalink>[A-Za-z0-9\-\_]+)$', views.viewpost, name='viewpost'),
    url(r'^page/(?P<permalink>[A-Za-z0-9\-\_]+)$', views.viewpage, name='viewpage'),
    url(r'^logout$', views.logoutview, name='logout'),
    url(r'^login$', views.loginview, name='login'),
    # url(r'^register$', views.registerview, name='register'),
    # url(r'^me$', views.accountsettings, name='account'),
    url(r'^(?P<category>[A-Za-z0-9\-\_]+)$', views.viewcategory, name='category'),
    url(r'^(?P<category>[A-Za-z0-9\-\_]+)/(?P<page>\d*[1-9]\d*)', views.viewcategory, name='categorypage')
]
