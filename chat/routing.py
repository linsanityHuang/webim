from django.conf.urls import url
from django.urls import path

from . import consumers

# 路由，指定 websocket 链接对应的 consumer
websocket_urlpatterns = [
	url(r'^wss/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
	url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
	# path('ws/chat/<str:room_name>/', consumers.ChatConsumer),
]
