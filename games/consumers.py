import json
from dataclasses import dataclass
from enum import Enum

from channels.generic.websocket import AsyncWebsocketConsumer

from games.models import Game


class MessageType(Enum):
    player_location_update = 0  # A player has entered, or exited, a location
    players_status_update = 1  # Player's statuses have changed, i.e. ALIVE, or ELIMINATED
    chat_message = 2  # A message in chat (could be something saying player A has joined the game)
    game_update = 3  # A change to the game, say a round is started, and at what time (so user clocks can sync)


@dataclass
class Message:
    type: MessageType  # The type of message being sent
    sender: str  # UID of the sender, use "" for messages from the server

    payload: any  # JSON body that is sent

    def serialize(self):
        d = self.__dict__
        d["type"] = self.type.name

        return d

    @staticmethod
    def decode(obj: dict):
        if "uid" in obj:
            obj["sender"] = obj["uid"]
        return Message.deserialize(obj)

    @staticmethod
    def deserialize(obj: dict):
        m = Message(
            type=MessageType[obj["type"]],
            sender=obj["sender"],
            payload=obj["payload"]
        )
        return m


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
        self.game = Game.objects.get(id=self.game_id)
        self.room_group_name = f"game_{self.game_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print(self.scope)

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
        pass
