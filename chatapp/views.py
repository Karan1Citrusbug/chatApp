from django.shortcuts import render
from .models import *


def home(request):
    return render(request,"home.html")

def room(request, room_name, user):
    try:
        avail_room = Room.objects.get(room=room_name)
        data = Chat.objects.filter(room = avail_room)
    except:
        print("no data found")
    context = {
        'data':data,
        'room_name': room_name,
        'user':user,
    }
    return render(request, 'room.html', context)
