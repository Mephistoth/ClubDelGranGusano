import json
from channels.generic.websocket import AsyncWebsocketConsumer

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat", self.channel_name)

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            "chat",
            {
                "type": "chat_message",
                "message": text_data,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=event["message"])