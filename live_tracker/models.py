from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass  # for now, no added fields



class Artist(models.Model):
    name = models.CharField(max_length=100)
    id = models.CharField(max_length=50,primary_key=True)
    def __str__(self):
        return self.name
    

class ArtistMetrics(models.Model):
    date = models.DateField()
    artist_name = models.CharField(max_length=100)
    artist_id = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    listeners = models.IntegerField()
    streams = models.IntegerField()
    streams_per_listener = models.FloatField()
    saves = models.IntegerField()
    playlist_adds = models.IntegerField()
    followers = models.IntegerField()
    total_active_audience = models.IntegerField()
    super_listeners = models.IntegerField()
    moderate_listeners = models.IntegerField()
    light_listeners = models.IntegerField()

    def __str__(self):
        return self.artist_name

