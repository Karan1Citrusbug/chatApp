from django.db import models

# Create your models here.

class Room(models.Model):
    room = models.CharField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    user = models.CharField(null=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
