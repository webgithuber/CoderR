from channels.consumer import SyncConsumer , AsyncConsumer
from asgiref.sync import async_to_sync
import time
import json

users={}
channels={}

class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self,event):
        print('websocket connceted...',event)
        self.send({
            'type':'websocket.accept',

        })
        
        roomname=self.scope['url_route']['kwargs']['roomname']
        username=self.scope['url_route']['kwargs']['username']
        print("connected user....",username ,roomname)
        print("channel name ...",self.channel_name)
        if roomname not in users:
            users[roomname]=[ ]
            channels[roomname]=[ ]
            
            
        users[roomname]+=[username]
        print("user in this room... " ,users[roomname])
        if len(channels[roomname])>0:
            print('channels_name' ,channels[roomname][0])
            async_to_sync(self.channel_layer.send)(
            channels[roomname][0],
            {
                'type':'new.join',
                'new_join':json.dumps({"new_join":self.channel_name}),
            }
        )
        channels[roomname]+=[self.channel_name]
        async_to_sync(self.channel_layer.group_add)(roomname,self.channel_name)
        async_to_sync(self.channel_layer.group_send)(roomname,{
            'type':'user.info',
            'list':json.dumps({"list":users[roomname]}),
            
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
            self.websocket_disconnect(event)
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
        users[roomname].remove(username)
        async_to_sync(self.channel_layer.group_discard)(roomname,self.channel_name)

        async_to_sync(self.channel_layer.group_send)(roomname,{
            'type':'user.info',
            'list':json.dumps({"list":users[roomname]}),
            
        })
    
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


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print('websocket connceted...')
    
    async def websocket_receive(self,event):
        print('websocket receive...')
    
    async def websocket_disconnect(self,event):
        print('websocket disconnceted...')
  
