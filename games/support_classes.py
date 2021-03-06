from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    """ Enum class MessageType desribes the type of message being passed """
    player_location_update = 0  # A player has entered, or exited, a location
    players_status_update = 1  # Player's statuses have changed, i.e. ALIVE, or ELIMINATED
    chat_message = 2  # A message in chat (could be something saying player A has joined the game)
    game_update = 3  # A change to the game, say a round is started, and at what time (so user clocks can sync)
    zone_fullness_update = 4  # Send along with player_location_updates to update a zones current fullness


@dataclass
class Message:
    """ Class that holds data and metadata about a message. Contains the message type, the sender UID and the message payload in the form of a JSON"""
    type: MessageType  # The type of message being sent
    sender: str  # UID of the sender, use "" for messages from the server

    payload: any  # JSON body that is sent

    def serialize(self):
        """ Method returns the integer representation of the MessageType variable contained within a message. """
        d = self.__dict__
        d["type"] = self.type.name

        return d

    @staticmethod
    def decode(obj: dict):
        """ Returns the deserialized information of the Message object passed as a parameter. Identifies the sender of the message and uses the function deserialize to provide the deserialized Message object """
        if "uid" in obj:
            obj["sender"] = obj["uid"]
        return Message.deserialize(obj)

    @staticmethod
    def deserialize(obj: dict):
        """ Deserializes a Message object. """
        m = Message(
            type=MessageType[obj["type"]],
            sender=obj["sender"],
            payload=obj["payload"]
        )
        return m