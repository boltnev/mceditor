import shutil
import re
from os import listdir
from os.path import isfile, join

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

# Create your models here.

def file_size(value): # add this to some file where you can import it from
    limit = 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MiB.')


class Chest(models.Model):

    title = models.CharField(
        verbose_name="Название ящика",
        max_length=100,
        null=False,
        blank=False,
    )

    coord_x = models.IntegerField(
        verbose_name="Координата X",
        blank=True,
        null=True
    )

    coord_y = models.IntegerField(
        verbose_name="Координата Y",
        blank=True,
        null=True
    )

    coord_z = models.IntegerField(
        verbose_name="Координата Z",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Волшебный ящик"
        verbose_name_plural = "Волшебные ящики"

    def __str__(self):
        return self.title


class Map(models.Model):

    title = models.CharField(
        verbose_name="Название",
        max_length=100,
        default="",
        null=False,
        blank=False,
    )

    file = models.FileField(
        verbose_name="Файл карты",
        upload_to="maps/",
        validators=[file_size]
    )

    number = models.IntegerField(
        verbose_name="номер",
        blank=True,
        null=True,
    )

    chest = models.ForeignKey(
        Chest,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=False,
    )

    class Meta:
        verbose_name = "Карта"
        verbose_name_plural = "Карты"

    def __str__(self):
        return self.title


@receiver(post_save, sender=Map)
def install_map(sender, instance, created, **kwargs):
    if not created:
        return
    list_files = [f for f in listdir(settings.MAPS_DST)
                  if isfile(join(settings.MAPS_DST, f))]
    if not list_files:
        new_number = 0
    else:
        pattern = re.compile(r"map_(\d+).dat")
        numbers = [int(re.match(pattern, f).group(1)) for f in list_files
                   if re.match(pattern, f)]
        new_number = max(numbers) + 1
    shutil.copy(instance.file.path, join(settings.MAPS_DST, "map_"+str(new_number)+".dat"))
    instance.number = new_number
    post_save.disconnect(install_map, sender=Map)
    try:
        instance.save()
    except:
        raise
    finally:
        post_save.connect(install_map, sender=Map)
