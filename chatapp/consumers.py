from channels.consumer import SyncConsumer , AsyncConsumer
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat.settings")
django.setup()
from .models import Room, ActiveUser
from django.contrib.auth.models import User

import time
import json



 

# Create a redis client

#redisClient = redis.StrictRedis(host='13.233.89.19',port=6379,db=0)

# Add values to the Redis list through the HEAD position of the list
# redisClient.lpush('LanguageList', "Kotlin")
# redisClient.lpush('LanguageList', "Python")
# print(redisClient.lindex('LanguageList', 0))
# print(redisClient.lindex('LanguageList', 1))


class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self,event):
        print('websocket connceted...',event)
        self.send({
            'type':'websocket.accept',

        })
        
        roomname=self.scope['url_route']['kwargs']['roomname']
        username=self.scope['url_route']['kwargs']['username']
        id=self.scope['url_route']['kwargs']['id']
        print("this user....",roomname,username)
        async_to_sync(self.channel_layer.group_add)(roomname,self.channel_name)
        async_to_sync(self.channel_layer.group_send)(roomname,{
            'type':'user.joined',
            'channel_name':self.channel_name,
            'added':json.dumps({"added":[id,username,"nothing"]}),
            
        })

        room=Room.objects.get(room_code=roomname)
        
        user_list=room.activeuser_set.all()
        list=[]
        print(user_list)
        for user in user_list:
            list.append([user.user.username,user.username,user.channelname])
        
        if len(list)>0:
            async_to_sync(self.channel_layer.send)(
            list[0][2],
            {
                'type':'new.join',
                'new_join':json.dumps({"new_join":self.channel_name}),
            })

        ActiveUser(room_code=room,
        user=User.objects.get(username=id),username=username,
        channelname=self.channel_name).save()

        list.append([id,username,"nothing"])
        print("recent list....",list)
        async_to_sync(self.channel_layer.send)(self.channel_name,
            {
                'type':'recent.list',
                'list':json.dumps({"list":list}),
            })
        

    def websocket_receive(self,event):
        print('websocket receive...' ,event)
        roomname=self.scope['url_route']['kwargs']['roomname']
        username=self.scope['url_route']['kwargs']['username']
        #print('messege is ',event['text'])
        print("user sending message...",username,roomname)
        obj=(json.loads(event['text']))
        if 'new_join' in obj:
            async_to_sync(self.channel_layer.send)(
            obj['new_join'],
            {
                'type':'recent.content',
                'msg':json.dumps({"msg":obj['msg']}),
            }
            )
        elif 'close' in obj:
            print('close')
        else:
            pass
            async_to_sync(self.channel_layer.group_send)(roomname,{
                'type':'chat.message',
                'message':event['text'],
                'channel_name':self.channel_name,
                
            })
        print('user', self.scope['user'].username)
    
    def websocket_disconnect(self,event):
        print('websocket disconnceted...')
        roomname=self.scope['url_route']['kwargs']['roomname']
        username=self.scope['url_route']['kwargs']['username']
        id=self.scope['url_route']['kwargs']['id']
        room=Room.objects.get(room_code=roomname)
        print("deleting ...",id,username)

        ActiveUser.objects.filter(room_code=room,
        channelname=self.channel_name).delete()

        
        async_to_sync(self.channel_layer.group_discard)(roomname,self.channel_name)
        async_to_sync(self.channel_layer.group_send)(roomname,{
            'type':'user.removed',
            'removed':json.dumps({"removed":[id,username,"nothing"]}),
            
        })
        

        raise StopConsumer()
    
    def chat_message(self,event):
        print('event... ', event)
        if self.channel_name!=event['channel_name']:
            self.send({
                'type':'websocket.send',
                'text':event['message']
            })
    def user_info(self,event):
        self.send({
                'type':'websocket.send',
                'text':event['list']
            })
    def user_joined(self,event):
        if self.channel_name!=event['channel_name']:
            self.send({
                    'type':'websocket.send',
                    'text':event['added']
                })
    def user_removed(self,event):
        self.send({
                'type':'websocket.send',
                'text':event['removed']
            })
    def new_join(self,event):
        self.send({
                'type':'websocket.send',
                'text':event['new_join']
            })
    def recent_content(self,event):
        self.send({
                'type':'websocket.send',
                'text':event['msg']
            })
    def recent_list(self,event):
        self.send({
                'type':'websocket.send',
                'text':event['list']
            })


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print('websocket connceted...')
    
    async def websocket_receive(self,event):
        print('websocket receive...')
    
    async def websocket_disconnect(self,event):
        print('websocket disconnceted...')
  
