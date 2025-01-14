from django.db import models
from users.models import User

class Station(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=90)
    handle = models.CharField(max_length=60, unique=True)
    description = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)
