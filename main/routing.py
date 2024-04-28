from .consumers import ChatConsumer
from django.urls import path


websocket_urlpatterns = [
    path('ws/chat/<int:room_id>/', ChatConsumer.as_asgi()),
]


