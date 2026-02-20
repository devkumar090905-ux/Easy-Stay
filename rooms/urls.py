from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),
    path("room/<int:id>/", views.room_detail, name="room_detail"),
    path("add-room/", views.add_room, name="add_room"),
]
