# livechat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import LiveChatSession, LiveChatMessage, CounselorProfile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # The room name will be the session ID, or a specific chat room ID
        # For simplicity, let's assume room_name is passed in the URL.
        # In a real system, you'd have logic to create/find a session
        # and assign user/counselor to it.
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Optional: Load chat history when user connects (for existing sessions)
        # You'd need to fetch messages for this session and send them
        # to the connected client.
        # messages = await self.get_session_messages(self.room_name)
        # for msg in messages:
        #     await self.send(text_data=json.dumps({
        #         'type': 'chat_message',
        #         'message': msg.message,
        #         'sender': msg.sender.username,
        #         'timestamp': str(msg.timestamp)
        #     }))


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # Optional: Mark session as inactive if it's the last participant
        # await self.mark_session_inactive(self.room_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = self.scope['user'].id # Get sender ID from authenticated user

        # Save message to database asynchronously
        await self.save_message(self.room_name, sender_id, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope['user'].username, # Sender's username
            }
        )

    # Receive message from room group (i.e., from another participant in the chat)
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    @database_sync_to_async
    def save_message(self, session_id, sender_id, message_content):
        session = LiveChatSession.objects.get(id=session_id)
        sender = User.objects.get(id=sender_id)
        LiveChatMessage.objects.create(session=session, sender=sender, message=message_content)

    # @database_sync_to_async
    # def get_session_messages(self, session_id):
    #     return list(LiveChatMessage.objects.filter(session_id=session_id).order_by('timestamp'))

    # @database_sync_to_async
    # def mark_session_inactive(self, session_id):
    #     session = LiveChatSession.objects.get(id=session_id)
    #     # You'd need more complex logic here to check if ALL participants have left
    #     session.is_active = False
    #     session.end_time = timezone.now()
    #     session.save()