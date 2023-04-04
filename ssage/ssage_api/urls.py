from django.urls import path
from django.conf.urls import include
from . import views
from . import routing

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.authtoken')),
    path('ws/', include(routing.websocket_urlpatterns)),
    path("chat/", views.index, name="index"),
    path("chat/<str:room_name>/", views.room, name="room"),



]
