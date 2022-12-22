from django.urls import path

from .import consumers


websocket_urlpatterns=[
    path('ws/sc/<str:roomname>/<str:username>/',consumers.MySyncConsumer.as_asgi()),
    path('ws/ac/',consumers.MyAsyncConsumer.as_asgi()),

]