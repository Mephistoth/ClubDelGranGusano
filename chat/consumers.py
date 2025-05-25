import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GranGusano.settings")
import django
django.setup()
# esto es porque... 
from channels.db import database_sync_to_async
from django.utils import timezone
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "general_chat"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('message', '').strip()
        if not message_text:
            return

        user = self.scope.get('user')
        is_auth = hasattr(user, 'is_authenticated') and user.is_authenticated
        username = (user.first_name or user.username) if is_auth else None

        # Guardar en BD sin bloquear el loop de eventos
        await database_sync_to_async(Message.objects.create)(
            user = user if is_auth else None,
            content = message_text,
            timestamp = timezone.now()
        )

        # Difundir a todos los conectados
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'user': username or "Invitado"
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user']
        }))