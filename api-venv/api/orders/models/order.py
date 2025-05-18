from django.db import models
from users.models import User
import uuid

class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    oid = models.CharField(default='', unique=True)
    tx_sig = models.CharField(unique=True)
    sol_value = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.oid:
            self.oid = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.oid)
