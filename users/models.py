import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

"""
The user model that represents a user participating in the game. 
Implemented using the built-in Django user model: AbstractUser.
"""

class User(AbstractUser):
    """ The User class that represents a user that has created an account.
    Implemented using the built-in Django user model 'AbstractUser'.
    The User class consists of an id that uniquely identifies a user. It uses a uuid in order to be more secure.
    It also contains a profile picture that is uploaded by the user.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)  # id uniquely identifies a user
    profile_picture = models.ImageField(default="", null=True)


class GameParticipation(models.Model):
    """
    Game Participation class represents information about a user currently participating in a game. This is useful because it provides an easy way to store data about users currently playing a game. The class consists of a User that is currently playing the game. A Game that the user is currently participating in. The current Zone that the user is in. A boolean value of whether the user is alive. A boolean value of whether the user is eliminated
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User that is currently participating in a game

    game = models.ForeignKey("games.Game", on_delete=models.CASCADE)  # What game is the user currently participating in
    current_zone = models.ForeignKey("games.Zone", on_delete=models.DO_NOTHING)  # What zone is the user currently in

    score = models.IntegerField(default=0)  # User score

    is_alive = models.BooleanField(default=False)  # Is the player alive
    is_eliminated = models.BooleanField(default=False)  # Is the player eliminated
