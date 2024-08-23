# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        user = data["user"]
        message = data["message"]
        room_name = data["room_name"]
        try:
            avail_room = Room.objects.get(room=room_name)
        except:
            avail_room = Room.objects.create(room = room_name)
        if user and message:
            Chat.objects.create(user = user,room=avail_room,message = message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,{'type':"chat_messages",'messages':message,'user':user,'room_name':room_name}
        )

    def chat_messages(self,event):
        message = event["messages"]
        user = event["user"]
        room_name = event["room_name"]
        self.send(text_data = json.dumps({"message":message ,"user":user, "room_name":room_name}))
