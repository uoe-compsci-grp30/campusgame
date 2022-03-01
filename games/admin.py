from django.contrib import admin

from games.models import Game, Round, Zone


# Register your models here.

class RoundInline(admin.TabularInline):
    model = Round
    filter_horizontal = ["active_zones"]


class GameAdmin(admin.ModelAdmin):
    inlines = [
        RoundInline,
    ]


admin.site.register(Game, GameAdmin)
admin.site.register(Round)
admin.site.register(Zone)
