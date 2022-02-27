from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_picture = models.ImageField(default="")


class GameParticipation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    game = models.ForeignKey("games.Game", on_delete=models.CASCADE)
    current_zone = models.ForeignKey("games.Zone", on_delete=models.DO_NOTHING)

    score = models.IntegerField(default=0)
    is_win = models.BooleanField(default=False)