from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.authtoken')),
]
