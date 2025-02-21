import uuid
from django.db import models
from django.utils.text import slugify
from .album import Album
from moods.models import Mood
from genres.models import Genre

class Track(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='tracks'
    )
    genres = models.ManyToManyField(Genre, related_name='tracks')
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=120, default='')
    bpm = models.CharField(default='')
    duration = models.IntegerField(default=0, blank=True, null=True)
    tid = models.CharField(default='', unique=True)
    slug = models.SlugField(blank=True, default='')
    order_no = models.IntegerField(default=0)
    is_exclusive_sold = models.BooleanField(blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    objects = models.Manager()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if not self.tid:
            self.tid = uuid.uuid4().hex
        super().save(*args, **kwargs)

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
