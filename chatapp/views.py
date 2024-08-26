from django.shortcuts import render,redirect
from .models import *
import json


def home(request):
    """
    **description**:
        dispay home page to user where user can provide details to enter chat room
    """
    try:
        avail_chat_room = Room.objects.all()
        return render(request,"home.html",{'avail_chat_room':avail_chat_room})        
    except:
        print("no chat room found")
        return render(request,"home.html")

def room(request, room_name:str, user:str):
    """
    **description**:
        display the room chat

    **perameter**:
        room_name:str
        user:str
    **Template**:
        room.html
    """
    try:
        avail_room = Room.objects.get(room=room_name)
    except:
        avail_room = Room.objects.create(room = room_name)
    data = Chat.objects.filter(room = avail_room)
    data_list = [{'user': obj.user, 'message': obj.message} for obj in data]
    context = {
        'data': json.dumps(data_list),
        'room_name': room_name,
        'user':user,
        }
    return render(request, 'room.html', context)
    
