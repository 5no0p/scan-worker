import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from event.services import new_ticket_check

scand_ticket = []

class EventConsumer(WebsocketConsumer):
    def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['event_id']
        # self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            # str(self.room_group_name),
            # self.channel_name
            "event",
            self.channel_name,
        )

        self.accept()
        
        async_to_sync(self.channel_layer.group_send)(
            "event",
                {
                    'type': 'scaned_ticket',
                    'update': 'connected',
                }
        )


        

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        # message = text_data_json["message"]
        # # if message["ticket_id"] not in scand_ticket:
        # #     scand_ticket+=[message["ticket_id"]]
        # #     ticket_check = new_ticket_check(**message)
        # #     contects = {"ticket_check_id": ticket_check}
        # # else: 
        # contects = f"ticket with id: {message['ticket_id']} alredy checked"
        # self.send(text_data=json.dumps(text_data))
        async_to_sync(self.channel_layer.group_send)(
            "event",
                {
                    'type': 'scaned_ticket',
                    'update': text_data_json
                }
        )
        

    def scaned_ticket(self, event):
        # text_data_json = json.loads(event)
        # content = text_data_json['update']
        # print("content: %s" % event['update'])
        # population = text_data_json['update']

        # print('payload: %s' % population)
        self.send(text_data=json.dumps(event))

        # Send message to WebSocket
        # self.send(text_data=json.dumps({
        #     # 'type': 'pop_message',
        #     'content': content,
        #     'population': population,

        # }))