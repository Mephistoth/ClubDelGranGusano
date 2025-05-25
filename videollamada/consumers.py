# videollamada/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'videollamada_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"🟢 Usuario conectado a sala {self.room_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"🔴 Usuario desconectado de sala {self.room_name}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"📩 Recibido en sala {self.room_name}: {data}")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': data
            }
        )

    async def send_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))