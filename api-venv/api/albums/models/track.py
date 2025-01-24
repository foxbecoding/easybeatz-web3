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
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, related_name='albums')
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=120, default='')
    tid = models.CharField(default='', unique=True)
    slug = models.SlugField(blank=True, default='')
    order_no = models.SmallIntegerField(default=0)
    is_exclusive_sold = models.BooleanField(blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if not self.tid:
            self.tid = uuid.uuid4().hex
        super().save(*args, **kwargs)
