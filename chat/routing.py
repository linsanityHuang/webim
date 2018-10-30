# chat/routing.py
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/user/(?P<channel_group_name>[^/]+)/$', consumers.ChatConsumer),
]
