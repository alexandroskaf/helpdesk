from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    users = models.ManyToManyField(User, related_name='rooms')

    def __str__(self):
        return self.name

class RoomUser(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('room', 'user'),)  # Ensure unique pairs of room and user

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    room_test = models.ForeignKey(Room, related_name='messages_test', on_delete=models.CASCADE, default="")

    content = models.TextField()
    file = models.FileField(upload_to='uploads/', blank=True)  # Add this line
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)
