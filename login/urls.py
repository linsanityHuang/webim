from django.conf.urls import url
from . import views

app_name = 'login'

urlpatterns = [
	# url('^$', views.home, name='home'),
	url(r'^do_login/$', views.do_login, name='do_login'),
	url(r'^signin/$', views.signin, name='signin'),
	url(r'^signup/$', views.signup, name='signup'),
]
