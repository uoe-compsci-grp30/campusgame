import uuid

from django.db import models
from django.contrib.gis.db.models import GeometryField


class Game(models.Model):
    # The game ID acts as a room name
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)

    # game_type = models.I
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField()

    max_participants = models.IntegerField(default=20)
    target_score = models.IntegerField(default=100)

    @property
    def current_round(self):
        # TODO: Make this implementation pick the current round by time
        return self.round_set.last()

    @property
    def next_round(self):
        # TODO: Make this implementation pick the current round by time -> round next in line
        return self.round_set.last()

    def start_game(self):
        """
        This method starts the current game.
        When a game is started, a celery task is created, which will act as the gamekeeper's assistant.

        The celery will manage the rounds, send scheduled messages to the user devices.

        The game is made up of multiple rounds. In each round, a set of zones are randomly selected, and players
        must visit as many of these zones as possible, as quick as they can, and must finish the round in a zone.

        When the timer goes off, then the worker will check all player's participation instance to see which
        users are in a zone.
        Users that are not in a zone will be marked as not alive, and will have to win a minigame to get back in.
        If they fail the minigame, then they are out of the game, and marked as eliminated.

        Before the end of each round, a warning will be sent to the players that they have x amount of time left.
        And 5 seconds before the end of each round, a message will be sent to the devices to remind them to check their
        location, and see if they're in a zone.

        Checking of location is done server-side, this would be the quickest way because of the extensive geo-indexing
        that PostGIS provides.
        """
        pass

    def get_player_statuses(self):
        participation_set = self.gameparticipation_set.all()
        alive_set = participation_set.filter(is_alive=True)
        eliminated_set = participation_set.filter(is_eliminated=True)
        dead_set = participation_set.exclude(is_alive=True, is_eliminated=True)

        return {
            "alive": alive_set.values_list(["user__uid"]),
            "dead": dead_set.values_list(["user__uid"]),
            "eliminated": eliminated_set.values_list(["user__uid"])
        }


class Round(models.Model):
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField()

    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    active_zones = models.ManyToManyField("games.Zone")


class Zone(models.Model):
    geometry = GeometryField()  # Polygon
    capacity = models.IntegerField()
