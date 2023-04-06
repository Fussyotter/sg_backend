from django.urls import re_path, path
from . import consumers
# https://channels.readthedocs.io/en/stable/introduction.html
websocket_urlpatterns = [
    # re_path(r'^ws/chat/$', consumers.DjoserAuthConsumer.as_asgi()),
    path('ws/chat/$', consumers.RealTimeChat.as_asgi()),


    # re_path(r'chat/$', consumers.ChatConsumerUserTest.as_asgi()),
    # re_path(r"chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),

]
