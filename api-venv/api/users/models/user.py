from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pubkey = models.CharField(max_length=32, blank=False, null=False, default='')
    username = models.CharField(max_length=70, blank=True, null=True, default='Unnamed')
    slug = models.SlugField(max_length=70, blank=True, null=True, unique=True)
    profile_image = models.CharField(max_length=200, blank=True, default='')
    profile_banner = models.CharField(max_length=200, blank=True, default='')
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True, default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.username:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username or ''

