from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path("ws/event", consumers.EventConsumer.as_asgi()),
]