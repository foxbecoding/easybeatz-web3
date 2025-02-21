from django.db import models
from .track import Track

class TrackPrice(models.Model):
    track = models.OneToOneField(
        Track,
        on_delete=models.CASCADE,
        related_name='price',
        primary_key=True,
    )
    value = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    objects = models.Manager()
