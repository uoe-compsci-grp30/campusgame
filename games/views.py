from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from games.models import Game
from games.serializers import GameSerializer


class GameViewSet(ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()

