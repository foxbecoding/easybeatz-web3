from django.db import models
from genres.models import Genre
from stations.models import Station
from django.utils.text import slugify

class Album(models.Model):
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='albums'
    )
    genres = models.ManyToManyField(Genre, related_name='albums')
    title = models.CharField(max_length=120, default='')
    aid = models.CharField(default='')
    slug = models.SlugField(blank=True, default='')
    bio = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
