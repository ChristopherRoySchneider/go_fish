from django.conf.urls import url
from . import views	# the . indicates that the views file can be found in the same directory as this file
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^add$', views.quote_add),
    url(r'^like$', views.quote_like),
    url(r'^delete$', views.quote_delete),
    url(r'^user/(?P<user_id>\d+)$', views.quote_user),
]
