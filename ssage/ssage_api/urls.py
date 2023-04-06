from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView
from . import views
from . import routing
from .views import send_message

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.authtoken')),
    path('ws/', include(routing.websocket_urlpatterns)),
    # path("chat/", views.ChatView.as_view(), name="index"),
    path('chat/<str:recipient_username>/', views.ChatView.as_view()),
    # TESTING ROUTES BELOW
    # path('chat/<str:recipient_username>/',
    #      TemplateView.as_view(template_name='chat/chat_test.html'), name='chat_test'),
    # path('send-message/<str:recipient_username>/',
    #      send_message, name='send_message'),



]
