from . import views
from django.conf.urls import url


urlpatterns = [
	url(r'^$', views.agent),
	url(r'^create_user/$', views.create_user, name='create_user'),
]