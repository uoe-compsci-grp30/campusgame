import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from games.models import Game
from games.support_classes import MessageType, Message


class GameConsumer(AsyncWebsocketConsumer):
    game_id = ""
    game = None
    room_group_name = ""

    def __init__(self):
        super(GameConsumer, self).__init__()
        self.msg_types = MessageType.__dict__.get("_member_names_", [])

    async def connect(self):
        # Connect to the game 'room'
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game = await database_sync_to_async(lambda x: Game.objects.get(id=x))(self.game_id)
        self.room_group_name = self.game.room_group_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        msg_type = text_data_json["type"]
        if not self.msg_types.__contains__(msg_type):
            return

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': msg_type,
                'message_d': text_data_json
            }
        )

    async def players_status_update(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': MessageType.chat_message.name,
                "message_d": Message(
                    type=MessageType.chat_message,
                    sender="",
                    payload=self.game.get_player_statuses()
                ).serialize()
            }
        )

    # Can be adapted for a game chat if you want, this just exists for the sake of it
    async def chat_message(self, event):
        message_d = event['message_d']

        message = Message.decode(message_d)
        # Do various things, such as check for naughty words

        # Broadcast message to WebSocket
        await self.send(text_data=json.dumps(message.serialize()))

    async def game_update(self, event):
        """
        This endpoint is called whenever a game update occurs.
        Most of this will be called from the back-end

        :param event:
        """
        message_d = event['message_d']

        message = Message.decode(message_d)
        # Do various things, such as check for naughty words

        # Broadcast message to WebSocket
        await self.send(text_data=json.dumps(message.serialize()))
