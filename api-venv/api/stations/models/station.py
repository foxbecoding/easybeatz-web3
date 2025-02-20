from django.db import models
from users.models import User

class Station(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=90, default="")
    handle = models.CharField(max_length=90, unique=True, default="")
    description = models.TextField(blank=True, default="")
    email = models.EmailField(max_length=254, unique=True, default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    objects = models.Manager()
    @property
    def picture_url(self):
        return self.picture.picture.url if self.picture else None

