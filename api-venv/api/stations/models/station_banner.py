from django.db import models
from .station import Station

class StationBanner(models.Model):
    station = models.OneToOneField(
        Station,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    file = models.FileField(upload_to='station/banner/')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)
    objects = models.Manager()
