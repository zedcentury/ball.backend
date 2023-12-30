import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']

        if user.is_anonymous:
            await self.close()
            return

        group_name = f'user_{user.id}'
        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        user = self.scope['user']

        if user.is_anonymous:
            await self.close()
            return

        group_name = f'user_{user.id}'
        await self.channel_layer.group_discard(
            group_name,
            self.channel_name
        )

    async def receive(self, **kwargs):
        text_data = kwargs.get('text_data')
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def notification_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
