# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from channels.layers import get_channel_layer
# from daphne.asgi import ASGIStaticFilesHandler
# from ssage_api.routing import websocket_urlpatterns
# from django.urls import re_path


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ssage.settings')

# application = ProtocolTypeRouter({
#     "http": ASGIStaticFilesHandler(get_asgi_application()),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })

# # Create a new variable for the channel layer
# channel_layer = get_channel_layer()

# # Wrap the application with the channel layer
# application = channel_layer.asgi()(application)
# import os
# from django.core.asgi import get_asgi_application
# from django.urls import re_path
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator
# import ssage_api.routing


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# # Initialize Django ASGI application early to ensure the AppRegistry
# # is populated before importing code that may import ORM models.
# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter(
#     {
#     "http": django_asgi_app,
#     # Just HTTP for now. (We can add other protocols later.)
#     "websocket": AllowedHostsOriginValidator(
#     AuthMiddlewareStack(
#         URLRouter(
#             ssage_api.routing.websocket_urlpatterns
#         ))
#     )
# })
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_main.settings')

application = get_asgi_application()