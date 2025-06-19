from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Sala única: acepta exactamente /ws/chat/
    re_path(r'^ws/chat/$', consumers.ChatConsumer.as_asgi()),
]
