from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^travels$', views.travels),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^addTrip$', views.addTrip),
    url(r'^register$', views.register),
    url(r'^destination/(?P<id>\d+)$', views.destination),
    url(r'^join/(?P<id>\d+)$', views.join)

]
