import json
import base64
import os
import time
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Room, Message
from django.conf import settings

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        username = data.get('username')
        room_slug = data.get('room')
        file_data = data.get('file')

        if file_data:
            file_name = await self.save_file(file_data)
            await self.save_message(username, room_slug, message, file_name)
        else:
            await self.save_message(username, room_slug, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'file': file_name if file_data else None
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        file_name = event.get('file')

        file_url = None
        if file_name:
            file_url = f"{settings.MEDIA_URL}{file_name}"  # Prepend MEDIA_URL to the file path

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'file': file_url  # Send the full file URL to the front end
        }))

    @sync_to_async
    def save_message(self, username, room_slug, message, file_name=None):
        user = User.objects.get(username=username)
        try:
            room_instance = Room.objects.get(slug=room_slug)
        except Room.DoesNotExist:
            print(f"Room with slug '{room_slug}' does not exist.")
            return

        msg = Message(user=user, room=room_instance, content=message)

        if file_name:
            msg.file = file_name

        msg.save()

    from django.conf import settings

    async def save_file(self, file_data):
        format, imgstr = file_data.split(';base64,')
        ext = format.split('/')[-1]
        timestamp = time.time()

        # Ensure the file is saved in the MEDIA_ROOT directory
        file_name = f'{timestamp}.{ext}'  # Unique name for the file
        file_path = os.path.join(settings.MEDIA_ROOT, 'chat_files', self.room_name, file_name)  # Save in MEDIA_ROOT

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(imgstr))

        # Return the relative path (without 'media/' because MEDIA_URL will handle it)
        return f'chat_files/{self.room_name}/{file_name}'


