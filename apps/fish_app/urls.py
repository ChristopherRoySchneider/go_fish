from django.conf.urls import url
from . import views	# the . indicates that the views file can be found in the same directory as this file
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^initialize$', views.initialize),
    url(r'^maingame$', views.maingame),
    url(r'^taketurn$', views.taketurn),
    url(r'^gameover$', views.gameover),
    url(r'^handover$', views.handover),
    url(r'^passcontrol$', views.passcontrol),
]
