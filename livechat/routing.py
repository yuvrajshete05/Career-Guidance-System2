# livechat/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # This assumes a 'room_name' (e.g., chat session ID) in the URL
    re_path(r'ws/livechat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]