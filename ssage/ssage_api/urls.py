from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView
from . import views
from . import routing

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.authtoken')),
    path('ws/', include(routing.websocket_urlpatterns)),
    path('chat/<str:recipient_username>/', views.ChatView.as_view()),
    path('chat/inbox/', views.InboxView.as_view()),
    path('messages/<int:message_id>/seen/', views.MessageUpdateView.as_view()),
    path('messages/<int:message_id>/', views.MessageDeleteView.as_view()),

    path('orders/', views.OrderList.as_view()),
    path('orders/<int:pk>', views.OrderDetail.as_view()),
    path('gifts/', views.GiftList.as_view()),

]

# path("chat/", views.ChatView.as_view(), name="index"),
# TESTING ROUTES BELOW
# path('chat/<str:recipient_username>/',
#      TemplateView.as_view(template_name='chat/chat_test.html'), name='chat_test'),
# path('send-message/<str:recipient_username>/',
#      send_message, name='send_message'),
