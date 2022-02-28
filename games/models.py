import uuid

from django.db import models
from django.contrib.gis.db.models import GeometryField


class Game(models.Model):
    # The game ID acts as a room name
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)

    # game_type = models.I
    start_dt = models.DateTimeField(auto_now_add=True)
    end_dt = models.DateTimeField()

    max_participants = models.IntegerField(default=20)
    target_score = models.IntegerField(default=100)

    def start_game(self):
        """
        This method starts the current game.
        When a game is started, a celery task is created, which will act as the gamekeeper's assistant.

        The celery will manage the rounds, send scheduled messages to the user devices
        """
        pass


class Round(models.Model):
    start_dt = models.DateTimeField(auto_now_add=True)
    end_dt = models.DateTimeField()

    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    active_zones = models.ManyToManyField("games.Zone")


class Zone(models.Model):
    geometry = GeometryField()  # Polygon
    capacity = models.IntegerField()
