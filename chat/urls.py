# chat/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^msg_gateway/$', views.msg_gateway),
	url(r'^chat_home/$', views.home, name='chat_home'),
	url(r'^init/$', views.init_user, name='init'),
	url(r'^init_group_chat/$', views.init_group_chat, name='init_group_chat'),
	url(r'^upload_image/$', views.upload_image, name='upload_image'),
	url(r'^add_friend/$', views.add_friend, name='add_friend'),
	url(r'^search_friend/$', views.search_friend, name='search_friend'),
	url(r'^modify_sign/$', views.modify_sign, name='modify_sign'),
	url(r'^group_chat_ids/$', views.group_chat_ids, name='group_chat_ids'),
]
