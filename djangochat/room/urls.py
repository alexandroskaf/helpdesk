from django.urls import path

from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),  # List of rooms
    path('create/', views.create_room, name='create_room'),  # Create a room
    path('<slug:slug>/', views.room, name='room'),  # Individual room by slug
]