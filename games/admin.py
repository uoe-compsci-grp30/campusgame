from django.contrib import admin

from games.models import Game, Round, Zone
# Register your models here.
admin.site.register(Game)

admin.site.register(Round)

admin.site.register(Zone)
