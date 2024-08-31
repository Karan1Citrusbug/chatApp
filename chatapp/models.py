from django.db import models

# Create your models here.

class Room(models.Model):
    room = models.CharField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    user = models.CharField(null=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField(null=True)
    img = models.ImageField(upload_to='images/', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
