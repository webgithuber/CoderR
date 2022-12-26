from channels.consumer import SyncConsumer , AsyncConsumer
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
import time
import json

users={}
channels={}
# import redis
# con = redis.Redis('13.233.89.19:5000')
# user = {"Name":"Pradeep", "Company":"SCTL", "Address":"Mumbai", "Location":"RCP"}
# con.hmset("pythonDict", {"Location": "Ahmedabad"})
# print(con.hgetall("pythonDict"))
class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self,event):
        print('websocket connceted...',event)
        self.send({
            'type':'websocket.accept',

        })
    
        roomname=self.scope['url_route']['kwargs']['roomname']
        username=self.scope['url_route']['kwargs']['username']
        id=self.scope['url_route']['kwargs']['id']
        ls=[]
        ls+=[id]
        ls+=[username]
        print("connected user....",username ,roomname)
        print("channel name ...",self.channel_name)
        print("list..", ls)
        if roomname not in users:
            users[roomname]=[ ]
        if roomname not in channels:
            channels[roomname]=[ ]
            
        users[roomname]+=[ls]
        print("channels...",channels)
        print("users...",users)
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

        ls=[]
        ls+=[id]
        ls+=[username]
        print("user in room....",users[roomname])
        print("removing..",ls)
        
        channels[roomname].remove(self.channel_name)
        users[roomname].remove(ls)
        print("user in room....",users[roomname])
        

        async_to_sync(self.channel_layer.group_discard)(roomname,self.channel_name)

        
        print("user len ....",len(users[roomname]))
        print("channels len ....",len(channels[roomname]))
        if len(users[roomname])==0:
            del users[roomname]
        else:
            async_to_sync(self.channel_layer.group_send)(roomname,{
            'type':'user.info',
            'list':json.dumps({"list":users[roomname]}),   
        })
        
        if len(channels[roomname])==0:
            del channels[roomname]
        
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
  
