from django.conf.urls import url
from . import views           
urlpatterns = [
  url(r'^$', views.index),
  url(r'^login$', views.login),
  url(r'^register$', views.register),
  url(r'^success$', views.success),
  url(r'^travels$', views.travels),
  url(r'^travels/add$', views.add),
  url(r'^travels/create$', views.create),
  url(r'^destination/(?P<id>\d+)$', views.destination),
  url(r'^travels/join/(?P<id>\d+)$', views.join),
  url(r'^destination/(?P<destination_id>\d+)/leave/(?P<user_id>\d+)$', views.leave),
  url(r'^logout$', views.logout)
]