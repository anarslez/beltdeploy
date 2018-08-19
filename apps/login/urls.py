from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^wishes$', views.wishes),
    url(r'^wishes/edit/(?P<id>\d+)$', views.edit),
    url(r'^wishes/update$', views.update),
    url(r'^wishes/new$', views.new),
    url(r'^wishes/add$', views.add),
    url(r'^wishes/stats$', views.stats),
    url(r'^wishes/delete/(?P<id>\d+)$', views.delete),
    url(r'^wishes/grant/(?P<id>\d+)$', views.grant),
    url(r'^wishes/like/(?P<id>\d+)$', views.like),
]