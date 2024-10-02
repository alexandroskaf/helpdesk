# from django.urls import path

# from . import views

# urlpatterns = [
#     path('', views.rooms, name='rooms'),  # List of rooms
#     path('create/', views.create_room, name='create_room'),  # Create a room
#     path('<slug:slug>/', views.room, name='room'),  # Individual room by slug
# ]
from django.urls import path
from .views import rooms, room, create_room
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('rooms/create/', create_room, name='create_room'),
    path('rooms/<slug:slug>/', room, name='room'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)