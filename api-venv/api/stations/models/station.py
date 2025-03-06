from django.db import models
from users.models import User
from datetime import datetime
from ..managers import StationManager

class Station(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=90)
    handle = models.CharField(max_length=90, unique=True)
    description = models.TextField(blank=True, default="")
    email = models.EmailField(max_length=254, unique=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    objects = models.Manager()
    stations = StationManager()

    @property
    def picture_url(self):
        return self.picture.picture_url if self.picture else None

    @property
    def formatted_launched_date(self):
        created_date = datetime.fromisoformat(str(self.created).replace("Z", "+00:00"))
        return f"Since {created_date.year}"
