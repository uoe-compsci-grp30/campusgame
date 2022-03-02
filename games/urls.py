from rest_framework import routers

from games.views import GameViewSet

router = routers.DefaultRouter()

router.register(r'games', GameViewSet)

urlpatterns = [

] + router.urls