from django.urls import path
from django.conf.urls import include
from . import views
from . import routing

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.authtoken')),
    path('ws/', include(routing.websocket_urlpatterns)),
    path("chat/", views.ChatView.as_view(), name="index"),
    path("chat/<str:room_name>/", views.ChatView.as_view(), name="room"),



]
