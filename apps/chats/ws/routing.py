from django.urls import path

from chats.ws.consumers import ChatConsumer

websocket_urls = [
    path('api/ws/chat', ChatConsumer.as_asgi(), name='ws_url')
]
