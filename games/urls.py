from django.urls import path, re_path
from rest_framework import routers

from games.views import GameViewSet, geolocation_zone_intersection_check

router = routers.DefaultRouter()

router.register(r'games', GameViewSet)

urlpatterns = \
    [
        re_path(
            r"^round/(?P<round_id>\d+)/zones/contains/(?P<longitude>[\s+-]?\d+(\.\d+)?)/(?P<latitude>[+-]?\d+(\.\d+)?)",
            geolocation_zone_intersection_check)
    ] + router.urls
