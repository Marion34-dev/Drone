from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/ap/receive_data/$', consumers.YourConsumer.as_asgi()),
]
