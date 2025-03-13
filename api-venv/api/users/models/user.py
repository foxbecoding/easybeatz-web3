from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pubkey = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=70, blank=True, null=True, unique=True)
    slug = models.SlugField(max_length=70, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.username:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.pubkey or ''

