# # loginform/asgi.py

# import os

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from django.core.asgi import get_asgi_application

# # Ensure Django settings are loaded
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginform.settings')
# import django
# django.setup() # Initialize Django's app registry

# # Import your application's routing (e.g., from app1/routing.py)
# # Make sure app1.routing.websocket_urlpatterns exists and is correct
# from app1 import routing


# application = ProtocolTypeRouter({
#     "http": get_asgi_application(), # Handles traditional HTTP requests (views, static files)
#     # Handles WebSocket connections
#     "websocket": AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter(
#                 routing.websocket_urlpatterns # This points to the WebSocket routes defined in app1/routing.py
#             )
#         )
#     ),
# })



# # loginform/asgi.py
# import os
# from django.core.asgi import get_asgi_application

# # Import Django Channels components
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack

# # Import your livechat's routing
# import livechat.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginform.settings') # Ensure 'loginform' matches your project name

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(), # Handles standard HTTP requests
#     "websocket": AuthMiddlewareStack( # Handles WebSocket requests
#         URLRouter(
#             livechat.routing.websocket_urlpatterns # Point to your livechat's WebSocket URLs
#         )
#     ),
# })




# loginform/asgi.py
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator # Good for security
from django.core.asgi import get_asgi_application

# Ensure Django settings are loaded
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginform.settings')

# Initialize Django's app registry. This is important for imports to work correctly.
import django
django.setup() 

# Import your application's routing (e.g., from app1/routing.py)
# You MUST create an app1/routing.py file if you don't have one.
from app1 import routing 


application = ProtocolTypeRouter({
    "http": get_asgi_application(), # Handles traditional HTTP requests (views, static files)
    # Handles WebSocket connections
    "websocket": AllowedHostsOriginValidator( # Helps prevent WebSocket connection from untrusted origins
        AuthMiddlewareStack( # Provides Django authentication for WebSockets
            URLRouter( # Routes WebSocket connections based on URL patterns
                routing.websocket_urlpatterns # This points to the WebSocket routes defined in app1/routing.py
            )
        )
    ),
})