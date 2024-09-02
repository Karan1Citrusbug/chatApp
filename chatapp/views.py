from django.shortcuts import render,redirect
from .models import *
import json
from django.urls import reverse
from django.http import JsonResponse
from .jwt_token import generate_jwt_token,decode_jwt_token
from django.shortcuts import redirect, render, HttpResponseRedirect, HttpResponse

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

def room(request, room_name:str, user:str,token:str):
    """
    **description**:
        display the room chat

    **perameter**:
        room_name:str
        user:str
    **Template**:
        room.html
    """
    decode = decode_jwt_token(token)
    
    # try:
    #     token = generate_jwt_token(user, room_name)
    #     return render(request,'room.html',{'token':token})
    # except:
    #     print("None")
    try:
        avail_room = Room.objects.get(room=decode["room"])
        auth = Chat.objects.filter(user = decode["user"],room=avail_room)
    except:
        avail_room = Room.objects.create(room=decode["room"])
    data = Chat.objects.filter(room = avail_room)
    data_list = [{'id':obj.id,'user': obj.user, 'message': obj.message,'chatimg':obj.img.url if obj.img else None} for obj in data]
    
    context = {
        'data': json.dumps(data_list),
        'room_name': room_name,
        'user':user,
        'token':token,
        }
    return render(request, 'room.html', context)
    

def deletemessage(request,id,token):
    chat = Chat.objects.get(pk=id)
    room_name = chat.room.room
    user = chat.user
    chat.message = "deleted"
    chat.save()
    return redirect('room', room_name=room_name, user=user,token=token)


def generate_token(request,user,room_name):
    token = generate_jwt_token(user, room_name)
    return JsonResponse({'token': token})