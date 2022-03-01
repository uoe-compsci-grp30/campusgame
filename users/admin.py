from django.contrib import admin

from users.models import User, GameParticipation
# Register your models here.
admin.site.register(User)
admin.site.register(GameParticipation)