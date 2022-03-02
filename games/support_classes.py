from dataclasses import dataclass
from enum import Enum


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