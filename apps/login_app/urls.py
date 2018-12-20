from django.conf.urls import url
# the . indicates that the views file can be found in the same directory as this file
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login_display$', views.login_display),
    url(r'^registration$', views.registration),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^myaccount$', views.myaccount),
    url(r'^update$', views.update),
]