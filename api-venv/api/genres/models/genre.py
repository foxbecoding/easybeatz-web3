from django.db import models
from django.utils.text import slugify

class Genre(models.Model):
    name = models.CharField(max_length=60, unique=True, default='')
    slug = models.SlugField(blank=True, default='')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()
    def save(self, *args, **kwargs): 
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
