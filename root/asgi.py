import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
django_asgi_application = get_asgi_application()

from chats.utils.jwt_auth_middleware_stack import JWTAuthMiddlewareStack
from chats.ws.routing import websocket_urls

application = ProtocolTypeRouter(
    {
        # 'http': get_asgi_application(),
        'websocket': JWTAuthMiddlewareStack(
            URLRouter(websocket_urls)
        )
    }
)
