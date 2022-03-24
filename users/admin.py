from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy

from users.models import User, GameParticipation


# Register your models here.
class MUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((gettext_lazy("Zones stuff"), {"fields": ("is_gamekeeper",)}),)


admin.site.register(User, MUserAdmin)
admin.site.register(GameParticipation)
