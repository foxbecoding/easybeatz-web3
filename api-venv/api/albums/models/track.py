from django.db import models
from django.utils.text import slugify
from .album import Album
from moods.models import Mood

class Track(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='tracks'
    )
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=120, default='')
    tid = models.CharField(default='', unique=True)
    slug = models.SlugField(blank=True, default='')
    order_no = models.SmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
