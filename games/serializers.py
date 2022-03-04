from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from games.models import Game, Zone, Round


class ZoneSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Zone
        geo_field = "geometry"
        fields = '__all__'


class RoundSimulator(serializers.ModelSerializer):
    active_zones = ZoneSerializer(many=True)

    class Meta:
        model = Round
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    rounds = serializers.SerializerMethodField()

    def get_rounds(self, instance: Game):
        return RoundSimulator(instance.round_set.all(), many=True).data

    class Meta:
        model = Game
        fields = '__all__'
