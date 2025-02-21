import uuid, os
from django.db import models
from .station import Station

def custom_image_upload_path(instance, filename):
    # Generate a unique filename using UUID
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('station/pictures/', new_filename)

class StationPicture(models.Model):
    station = models.OneToOneField(
        Station,
        on_delete=models.CASCADE,
        related_name='picture',
        primary_key=True,
    )
    picture = models.ImageField(upload_to=custom_image_upload_path, default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)
    objects = models.Manager()

    @property
    def picture_url(self):
        return self.picture.url if self.picture else None
