import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from django.shortcuts import get_object_or_404


class ChatConsumer(WebsocketConsumer):
    def connect(self): # 讓連接到相同聊天室的使用者連到相同名稱的Group
        # Group取名
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_name}"

        # 使用者加入Group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code): # 離開Group (但這樣就不能跳通知了)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # 前端在傳送訊息後惠存到資料庫，並發送同樣的訊息給consumers.receive接收，再經由函數chat_message發送給相同Group的其他人
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_id = text_data_json['message']
        new_message = get_object_or_404(Message,id=message_id)
        context = {
            "id":new_message.id,
            "context":new_message.context,
            "time": new_message.time.isoformat(),
            "senter": new_message.senter.user.username,
        }
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message', #type是指運用的函數，這邊是發送給相同頻道其他使用者
                'message': context
            }
        )

    # 發送訊息
    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message
        }))