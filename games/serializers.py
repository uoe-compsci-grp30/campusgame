from django.contrib.gis.db.models import Collect
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField

from games.models import Game, Zone, Round


class ZoneSerializer(GeoFeatureModelSerializer):
    fullness = serializers.SerializerMethodField()

    def get_fullness(self, instance: Zone):
        r = instance.round_set.get(pk=self.context["round_id"])  # type: Round
        idx = r.get_fullness_idx_for_zone_id(instance.id)
        return r.zone_fullness[idx]

    class Meta:
        model = Zone
        geo_field = "geometry"
        fields = ['fullness', 'capacity', 'pk']


class RoundSerializer(serializers.ModelSerializer):
    active_zones = serializers.SerializerMethodField()

    def get_active_zones(self, instance: Round):
        return ZoneSerializer(many=True, context={"round_id": instance.id}).to_representation(instance.active_zones)

    class Meta:
        model = Round
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    rounds = serializers.SerializerMethodField()
    ws_url = serializers.SerializerMethodField()

    def get_rounds(self, instance: Game):
        return RoundSerializer(instance.round_set.all(), many=True).data

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
