from django.contrib.gis.db.models import Collect
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField

from games.models import Game, Zone, Round


class ZoneSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Zone
        geo_field = "geometry"
        fields = ['capacity', 'pk']


class RoundSimulator(serializers.ModelSerializer):
    active_zones = ZoneSerializer(many=True)

    class Meta:
        model = Round
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    rounds = serializers.SerializerMethodField()
    ws_url = serializers.SerializerMethodField()

    def get_rounds(self, instance: Game):
        return RoundSimulator(instance.round_set.all(), many=True).data

    def get_ws_url(self, instance: Game):
        req = self.context.get('request')
        if req is None:
            return ""

        meta = req.META

        secure = req.scheme == "https"
        url = f"{'wss' if secure else 'ws'}://{meta['HTTP_HOST']}/ws/game/{instance.id}/"
        return url

    class Meta:
        model = Game
        fields = '__all__'
