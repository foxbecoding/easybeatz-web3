from django.db import models
from django.utils.text import slugify
from stations.models import Station
from ..managers import AlbumManager
from datetime import datetime
import uuid

class Album(models.Model):
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='albums'
    )
    title = models.CharField(max_length=120)
    aid = models.CharField(default='', unique=True)
    slug = models.SlugField(blank=True, default='')
    bio = models.TextField(blank=True, default='')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    objects = models.Manager()
    albums = AlbumManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if not self.aid:
            self.aid = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.aid)

    @property
    def uploaded_at(self):
        created_date = datetime.fromisoformat(str(self.created).replace("Z", "+00:00"))
        return f"Uploaded {created_date.year}"

    @property
    def tracks_count(self):
        return self.tracks.count()
