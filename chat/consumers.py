from channels.db import database_sync_to_async
from django.utils import timezone
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "general_chat"
        # >>> DEBUG: loguear intento de conexión
        print(f"[ChatConsumer] connect: channel_name={self.channel_name}")
        try:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            print(f"[ChatConsumer] connect: ACCEPTED {self.channel_name}")
        except Exception as e:
            print(f"[ChatConsumer] connect: ERROR {e}")
            await self.close(code=1011)

    async def disconnect(self, close_code):
        # >>> DEBUG: loguear desconexión
        print(f"[ChatConsumer] disconnect: channel_name={self.channel_name}, code={close_code}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # >>> DEBUG: loguear llegada de mensaje crudo
        print(f"[ChatConsumer] receive raw: {text_data}")
        try:
            data = json.loads(text_data)
            message_text = data.get('message', '').strip()
        except json.JSONDecodeError as e:
            print(f"[ChatConsumer] receive: JSON error {e}")
            return

        if not message_text:
            print("[ChatConsumer] receive: empty message, ignored")
            return

        user = self.scope.get('user')
        is_auth = getattr(user, 'is_authenticated', False)
        username = (user.first_name or user.username) if is_auth else "Invitado"

        # >>> DEBUG: loguear mensaje procesado antes de guardar
        print(f"[ChatConsumer] receive: user={username}, message={message_text}")

        # Guardar en BD
        await database_sync_to_async(Message.objects.create)(
            user=user if is_auth else None,
            content=message_text,
            timestamp=timezone.now()
        )

        # Difundir
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'user': username
            }
        )

    async def chat_message(self, event):
        # >>> DEBUG: loguear evento de grupo antes de enviar al cliente
        print(f"[ChatConsumer] chat_message event: {event}")
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user']
        }))