# chat/urls.py
from . import views
from django.conf.urls import url


urlpatterns = [
	url(r'^msg_gateway/$', views.msg_gateway),
	url(r'^chat_pc/$', views.chat_pc, name='chat_pc'),
	url(r'^chat_mobile/$', views.chat_mobile, name='chat_mobile'),
	url(r'^init/$', views.init_user, name='init'),
	url(r'^init_group_chat/$', views.init_group_chat, name='init_group_chat'),
	url(r'^upload_image/$', views.upload_image, name='upload_image'),
	url(r'^upload_file/$', views.upload_file, name='upload_file'),
	url(r'^add_friend/$', views.add_friend, name='add_friend'),
	url(r'^apply_group_chat/$', views.apply_group_chat, name='apply_group_chat'),
	url(r'^search_friend/$', views.search_friend, name='search_friend'),
	url(r'^modify_sign/$', views.modify_sign, name='modify_sign'),
	url(r'^group_chat_ids/$', views.group_chat_ids, name='group_chat_ids'),
	url(r'^modify_status/$', views.modify_status, name='modify_status'),
	url(r'^add_group_chat/$', views.add_group_chat, name='add_group_chat'),
	url(r'^add_group/$', views.add_group, name='add_group'),
	url(r'^user_info/$', views.user_info, name='user_info'),
	url(r'^upload_avatar/$', views.upload_avatar, name='upload_avatar'),
	url(r'^history_msg/$', views.history_msg, name='history_msg'),
]
