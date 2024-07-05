from django.urls import path
from .views import ThreadList, ThreadDetail, add_message, start_thread

messenger_patterns = ([
    path("", ThreadList.as_view(), name="list"),
    path("thread/<int:pk>", ThreadDetail.as_view(), name="detail"),
    path("thread/<int:pk>/add/", add_message, name="add"), #con add añadimos el thread o hilo y luego lo pasamos con un GET
    path("thread/start/<username>/", start_thread, name="start"),
], "messenger")