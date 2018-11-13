from . import views
from django.conf.urls import url

app_name = 'login'

urlpatterns = [
	url(r'^do_login/$', views.do_login, name='do_login'),
	url(r'^do_logout/$', views.do_logout, name='do_logout'),
	url(r'^signin/$', views.signin, name='signin'),
	url(r'^signup/$', views.signup, name='signup'),
]


