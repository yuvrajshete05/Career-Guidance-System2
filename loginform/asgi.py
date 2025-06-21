# loginform/asgi.py

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

# Ensure Django settings are loaded
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginform.settings')
import django
django.setup() # Initialize Django's app registry

# Import your application's routing (e.g., from app1/routing.py)
# Make sure app1.routing.websocket_urlpatterns exists and is correct
from app1 import routing


application = ProtocolTypeRouter({
    "http": get_asgi_application(), # Handles traditional HTTP requests (views, static files)
    # Handles WebSocket connections
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns # This points to the WebSocket routes defined in app1/routing.py
            )
        )
    ),
})