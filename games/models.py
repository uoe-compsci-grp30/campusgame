from django.db import models
from django.contrib.gis.db.models import GeometryField


class Game(models.Model):
    # game_type = models.I
    start_dt = models.DateTimeField(auto_now_add=True)
    end_dt = models.DateTimeField()

    max_participants = models.IntegerField(default=20)
    target_score = models.IntegerField(default=100)


class Round(models.Model):
    start_dt = models.DateTimeField(auto_now_add=True)
    end_dt = models.DateTimeField()

    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    active_zones = models.ManyToManyField("games.Zone")


class Zone(models.Model):
    geometry = GeometryField()  # Polygon
    capacity = models.IntegerField()
