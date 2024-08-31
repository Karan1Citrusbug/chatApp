# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
from django.core.files.base import ContentFile
import base64

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        """
        **description**:
            connecting the websocket
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        """
        **description**:
            disconnecting the websocket
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,self.channel_name
        )
        
    def receive(self, text_data):
        data = json.loads(text_data)
        user = data.get("user")
        message = data.get("message")
        chatimg_base64 = data.get("chatimg")
        status = data.get("status")
        
        if chatimg_base64:
            if ';base64,' in chatimg_base64:
                try:
                    format, imgstr = chatimg_base64.split(';base64,')
                    img_data = ContentFile(base64.b64decode(imgstr), name='image.' + format.split('/')[-1])
                except ValueError:
                    print("Invalid Base64 format")
                    img_data = None
            else:
                print("No Base64 delimiter found")
                img_data = None
        else:
            img_data = None

        avail_room = Room.objects.get(room=self.room_name)
        if (user and message) or (user and chatimg_base64):
            Chat.objects.create(user=user, room=avail_room, message=message, img=img_data)
            print("created")

        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {'type': "chat_messages", 'messages': message, 'user': user, 'room_name': self.room_name, "status": status, "chatimg": chatimg_base64}
        )

    def chat_messages(self,event):
        message = event["messages"]
        user = event["user"]
        status = event["status"]
        chatimg = event["chatimg"]
        self.send(text_data = json.dumps({"message":message ,"user":user, "room_name":self.room_name,"status":status,"chatimg":chatimg}))
