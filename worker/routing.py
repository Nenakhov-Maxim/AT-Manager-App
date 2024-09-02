from django.urls import path

from .consumers import VideoConsumer

ws_urlpatterns = [ 
  path('ws/video/<str:room_name>', VideoConsumer.as_asgi()),
]