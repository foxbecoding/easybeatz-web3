import uuid
from django.db import models
from stations.models import Station
from django.utils.text import slugify

class Album(models.Model):
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='albums'
    )
    title = models.CharField(max_length=120, default='')
    aid = models.CharField(default='', unique=True)
    slug = models.SlugField(blank=True, default='')
    bio = models.TextField(blank=True, default='')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if not self.aid:
            self.aid = uuid.uuid4().hex
        super().save(*args, **kwargs)
