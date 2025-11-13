import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_group_name = f"chat_{self.user_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)

        sender = User.objects.get(id=data["sender"])
        receiver = User.objects.get(id=data["receiver"])
        content = data["content"]

        # store message
        ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            content=content
        )

        # broadcast message
        await self.channel_layer.group_send(
            f"chat_{receiver.id}",
            {
                "type": "chat_message",
                "sender": sender.id,
                "receiver": receiver.id,
                "content": content
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
