from django.contrib.gis.geos import Point
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from games.models import Game, Round
from games.serializers import GameSerializer


class GameViewSet(ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


def geolocation_zone_intersection_check(request, *args, **kwargs):
    if request.method == "GET":
        round_id = kwargs.get("round_id")
        t_round = get_object_or_404(Round, id=round_id)

        latitude = float(kwargs.get("latitude"))
        longitude = float(kwargs.get("longitude"))

        p = Point((longitude, latitude), srid=4326)
        zones = t_round.active_zones.filter(geometry__intersects=p)

        if zones.count() > 0:
            return JsonResponse({
                "zone_id": zones.first().id  # Just return the first hit
            }, status=200)
        return JsonResponse({}, status=404)  # Location/zone ID was technically not found
