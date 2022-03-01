import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    profile_picture = models.ImageField(default="")


class GameParticipation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    game = models.ForeignKey("games.Game", on_delete=models.CASCADE)
    current_zone = models.ForeignKey("games.Zone", on_delete=models.DO_NOTHING)

    score = models.IntegerField(default=0)

    is_alive = models.BooleanField(default=False)  # Is the player alive
    is_eliminated = models.BooleanField(default=False)  # Is the player eliminated
