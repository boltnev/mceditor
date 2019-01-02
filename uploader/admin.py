import subprocess

from django.conf import settings
from django.contrib import admin
from .models import Map, Chest

from django.contrib.auth.models import User, Group


# Register your models here.
def place_map(modeladmin, request, qs):
    for map in qs:
        chest = map.chest
        subprocess.Popen([
            settings.INSTALL_MAP_SCRIPT,
            map.title,
            str(map.number),
            str(chest.coord_x),
            str(chest.coord_z),
            str(chest.coord_y),
            str(map.number % 27)
        ])
place_map.short_description = "Положить карту в ящик"


class MapAdmin(admin.ModelAdmin):
    list_display = ("title", "number",)
    readonly_fields = ("number",)
    actions = [place_map]


class ChestAdmin(admin.ModelAdmin):
    list_display = ("title", "coord_x", "coord_y", "coord_z")


admin.site.register(Map, MapAdmin)
admin.site.register(Chest, ChestAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)
