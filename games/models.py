import uuid

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.validators import int_list_validator
from django.db import models
from django.contrib.gis.db.models import GeometryField, Union, Collect
from django.utils import cache
from django.core.cache import cache

from games.support_classes import MessageType

class Game(models.Model):
    """
    Game class that represents a single game consisting of multiple rounds, being played by multiple users simultaneously.
    Each game consists of an id uniquely identifying it. A start and end date. The maximum number of participants. The target score of the game, once this score is reached the game ends and the user that reached this score first wins the game. The index of the current round that the game is on.
    """
    # The game ID acts as a room name
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)

    # game_type = models.I
    start_dt = models.DateTimeField() #datetime encoding of when the game starts
    end_dt = models.DateTimeField() #datetime encoding of when the game ends

    max_participants = models.IntegerField(default=20) #maximum participants in one game
    target_score = models.IntegerField(default=100) #target score of game
    current_round_idx = models.IntegerField(default=0) #the index represents what round of the game is currently being played -1

    @property
    def current_round(self):
        """Returns the value of the current round that the game is on"""
        if self.round_set.count() > 0:
            return self.round_set.all()[self.current_round_idx]
        return None

    @property
    def next_round(self):
        """Increases the round of the game by 1, to represent moving on to the next round"""
        if self.current_round_idx < self.round_set.count():
            return self.round_set.all()[self.current_round_idx + 1]
        return None

    @property
    def room_group_name(self):
        """Returns a formatted string of the game along with its primary key"""
        return f"game_{self.pk}"

    def start_game(self):
        """
        This method starts the current game.
        When a game is started, a celery task is created, which will act as the gamekeeper's assistant.

        The celery will manage the rounds, send scheduled messages to the user devices.

        The game is made up of multiple rounds. In each round, a set of zones are randomly selected, and players
        must visit as many of these zones as possible, as quick as they can, and must finish the round in a zone.

        When the timer goes off, then the worker will check all player's participation instance to see which
        users are in a zone.
        Users that are not in a zone will be marked as eliminated.

        Before the end of each round, a warning will be sent to the players that they have x amount of time left.
        And 5 seconds before the end of each round, a message will be sent to the devices to remind them to check their
        location, and see if they're in a zone.

        Checking of location is done server-side, this would be the quickest way because of the extensive geo-indexing
        that PostGIS provides.
        """

        # Create schedules for all the default events

        # Broadcast game start
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            self.room_group_name,
            {
                "type": MessageType.chat_message.name,
                "message_d": {
                    "type": MessageType.game_update.name,
                    "payload": {
                        "round_number": self.current_round_idx,
                        "started": True,
                        "ended": False
                    },
                    "uid": ""
                }
            }
        )

        pass

    def move_to_next_round(self):
        pass

    
    def get_player_statuses(self):
        """ Gets the statuses of players. A player can either be alive (participating in game as normal), eliminated (eliminated from the game) or dead (they can play a minigame in order to attempt to reenter the game) """
        participation_set = self.gameparticipation_set.all()
        alive_set = participation_set.filter(is_alive=True) #Set of alive players
        eliminated_set = participation_set.filter(is_eliminated=True) #Set of eliminated players
        dead_set = participation_set.exclude(is_alive=True, is_eliminated=True) #Set of players that can play a minigame to reenter game

        return {
            "alive": alive_set.values_list(["user__uid"]),
            "dead": dead_set.values_list(["user__uid"]),
            "eliminated": eliminated_set.values_list(["user__uid"])
        }

class Round(models.Model):
    """
    Round class represents an individual Round within a Game which can hold multiple rounds. A round is a set amount of time wherein users need to get into an active or safe zone, that has not yet reached full capacity. If when the round ends they are in one of these zones then they are safe, earn points and can continue unhindered with the game.
    Each Round object consists of a start and endtime. A Game that it is a part of. A set of active Zones. The fullness of each Zone.
    """
    start_dt = models.DateTimeField() #Start of the round
    end_dt = models.DateTimeField() #End of the round

    game = models.ForeignKey("Game", on_delete=models.CASCADE) #The game that the round is a part of
    active_zones = models.ManyToManyField("games.Zone") #The active zones in this round
    _zone_fullness = models.CharField(validators=[int_list_validator], max_length=200) #The number of players in a zone. Once a zone has reached full capacity, any additional players arriving at this zone are not safe, and need to be in a different active zone before the timer runs out to be considered safe.

    def get_fullness_idx_for_zone_id(self, z_id):
        """ Returns the fullness of a zone, with the zone being identified by its id. """
        idcs = self.active_zones.all().order_by("id").values_list("id", flat=True)
        return list(idcs).index(z_id)

    @property
    def zone_fullness(self):
        """ Returns the fullness of a zone, with the zone object being used to identify the zone. """
        return [int(x) for x in self._zone_fullness.split(",")]

    @zone_fullness.setter
    def zone_fullness(self, v: [int]):
        """ Sets the fullness of a zone, with the name used to identify the zone. """
        self._zone_fullness = ','.join([str(x) for x in v])


class Zone(models.Model):
    """
    Zone class that represents an area of space on the campus of Exeter. Each Zone can be made to be active or safe and if users are in this zone when a round ends then they receive points and stay in the game.
    A Zone consists of a polygon that represents the area it represents and a capacity which is the maximum number of players that it can hold at once.
    """
    geometry = GeometryField()  # Polygon
    capacity = models.IntegerField() #capacity of a zone
