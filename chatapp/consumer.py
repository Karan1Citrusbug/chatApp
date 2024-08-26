# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *

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
        """
        **description**:
            recive messages sent by the users
        """
        data = json.loads(text_data)
        user = data["user"]
        message = data["message"]
        avail_room = Room.objects.get(room=self.room_name)
        if user and message:
            Chat.objects.create(user = user,room=avail_room,message = message)
            print("created")
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,{'type':"chat_messages",'messages':message,'user':user,'room_name':self.room_name}
        )

    def chat_messages(self,event):
        message = event["messages"]
        user = event["user"]
        self.send(text_data = json.dumps({"message":message ,"user":user, "room_name":self.room_name}))
