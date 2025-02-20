from django.db import models
import uuid

class UserLoginNonce(models.Model):
    pubkey = models.CharField(max_length=100, unique=False)
    nonce = models.CharField(max_length=36, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    objects = models.Manager()
    def save(self, *args, **kwargs):
        self.nonce = str(uuid.uuid4())

        # Call the parent class's save method
        super().save(*args, **kwargs)
