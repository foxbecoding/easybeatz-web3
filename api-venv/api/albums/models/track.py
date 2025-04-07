import uuid
from django.db import models
from django.utils.text import slugify
from ..managers import TrackManager
from .album import Album
from moods.models import Mood
from genres.models import Genre
from datetime import datetime

class Track(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='tracks'
    )
    genres = models.ManyToManyField(Genre, related_name='tracks')
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=120)
    bpm = models.CharField()
    duration = models.IntegerField(default=0, blank=True, null=True)
    tid = models.CharField(unique=True)
    slug = models.SlugField(blank=True, default='')
    order_no = models.IntegerField(default=0)
    is_exclusive_sold = models.BooleanField(blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    objects = models.Manager()
    tracks = TrackManager()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if not self.tid:
            self.tid = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.tid)

    @property
    def uploaded_at(self):
        created_date = datetime.fromisoformat(str(self.created).replace("Z", "+00:00"))
        return f"{created_date.year}"

    @property
    def display_url(self):
        return self.display.audio.url if self.display else None
    
    @property
    def formatted_duration(self):
        hours, remainder = divmod(self.duration, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{hours}:{minutes:02}:{seconds:02}"
        return f"{minutes}:{seconds:02}"
