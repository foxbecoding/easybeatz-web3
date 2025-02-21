from django.db import models
from .track import Track
from stations.models import Station

class TrackCollaborator(models.Model):
    track = models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        related_name='collaborators'
    )
    station = models.OneToOneField(Station, on_delete=models.SET_NULL, blank=True, null=True, related_name='collaborations')
    pubkey = models.CharField(max_length=100, default='')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    objects = models.Manager()
