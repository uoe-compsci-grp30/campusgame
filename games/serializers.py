from django.conf import settings
from django.contrib.gis.db.models import Collect
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField

from games.models import Game, Zone, Round


class ZoneSerializer(GeoFeatureModelSerializer):
    """ Class is responsible for serializing a zone. """
    fullness = serializers.SerializerMethodField()

    def get_fullness(self, instance: Zone):
        """ Finds the fullness of a zone. """
        r = instance.round_set.get(pk=self.context["round_id"])  # type: Round
        idx = r.get_fullness_idx_for_zone_id(instance.id) #fullness of the zone
        return r.zone_fullness[idx]

    class Meta:
        """ Provides location to store metadata about the ZoneSerializer class. """
        model = Zone
        geo_field = "geometry"
        fields = ['fullness', 'capacity', 'pk']


class RoundSerializer(serializers.ModelSerializer):
    """ Class is responsible for serializing a round. """
    active_zones = serializers.SerializerMethodField()

    def get_active_zones(self, instance: Round):
        """ Finds the active zones using Zoneserializer. """
        return ZoneSerializer(many=True, context={"round_id": instance.id}).to_representation(instance.active_zones)

    class Meta:
        """ Provides the location to store metadata about the roundserializer class. """
        model = Round
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    """ Class is responsible for Serialiazing a game. """
    rounds = serializers.SerializerMethodField()
    ws_url = serializers.SerializerMethodField()

    def get_rounds(self, instance: Game):
        """ Returns the round that the game is on. """
        return RoundSerializer(instance.round_set.all(), many=True).data

    def get_ws_url(self, instance: Game):
        """ Returns the url, after performing authentication checks. """
        req = self.context.get('request')
        if req is None:
            return ""

        meta = req.META

        secure = not settings.DEBUG
        url = f"{'wss' if secure else 'ws'}://{meta['HTTP_HOST']}/ws/game/{instance.id}/"
        return url

    class Meta:
        """ Provides location to store metadata about the GameSerializer class. """
        model = Game
        fields = '__all__'
