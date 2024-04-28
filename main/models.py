from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from user.models import UserProfile

# Create your models here.

class Chatroom(models.Model):
    name = models.CharField(max_length=200, null=True)
    members = models.ManyToManyField(UserProfile,related_name='member',blank=True) # 一個使用者可以有多個關聯的聊天室

class Message(models.Model):
    context = models.CharField(max_length=200,help_text="enter your message")
    time =  models.DateTimeField(auto_now_add=True)
    senter = models.ForeignKey(UserProfile,related_name="sender",on_delete=models.CASCADE, null=True) # 一個使用者可以有多個關聯的訊息
    room = models.ManyToManyField(Chatroom,related_name="room") # 一個聊天室可以有多個關聯訊息

    class Meta:
        ordering = ['-id']  # 降序排列

    
