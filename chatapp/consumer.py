# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
from django.core.files.base import ContentFile
import base64
from .jwt_token import decode_jwt_token

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        """
        **description**:
            connecting the websocket
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.token = self.scope['url_route']['kwargs']['token']
        decode = decode_jwt_token(self.token)
        try:
            avail_room = Room.objects.get(room=decode["room"])
            if avail_room:
                auth = Chat.objects.filter(user = decode["user"],room=avail_room)
                if auth:
                    print("authorised")
                    async_to_sync(self.channel_layer.group_add)(
                        self.room_name,self.channel_name
                    )
                    self.accept()
                else:
                    print("unauthorized")
            else:
                print("no room available")
        except:
            print("unable to connect")

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
            process received data from the socket ,save in
        """
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
            chat = Chat.objects.create(user=user, room=avail_room, message=message, img=img_data)
            print("created")
            if chat:
                chat_id = chat.id
                async_to_sync(self.channel_layer.group_send)(
                    self.room_name, {'type': "chat_messages",'messages': chat.message, 'user': chat.user,"chat_id": chat_id ,'room_name': self.room_name, "status": status, "chatimg": chatimg_base64}
                )
        elif(status==True):
            async_to_sync(self.channel_layer.group_send)(
                self.room_name, {'type': "chat_messages",'messages': message, 'user': user, 'room_name': self.room_name, "status": status, "chatimg": chatimg_base64}
            )
        
        

    def chat_messages(self,event):
        message = event.get("messages")
        user = event.get("user")
        status = event.get("status")
        chatimg = event.get("chatimg")
        chat_id = event.get("chat_id")
        self.send(text_data = json.dumps({"message":message ,"chat_id":chat_id,"user":user, "room_name":self.room_name,"status":status,"chatimg":chatimg}))
