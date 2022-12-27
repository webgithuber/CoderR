from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Room(models.Model):
    room_code=models.CharField(max_length=10)
    lang=models.CharField(max_length=20,null=True)
class ActiveUser(models.Model):
    room_code=models.ForeignKey(Room,max_length=10,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User,max_length=20,on_delete=models.CASCADE,null=True)
    username=models.CharField(max_length=20,null=True)
    channelname=models.CharField(max_length=100,null=True)
