import uuid, os
from django.db import models
from .album import Album

def custom_image_upload_path(instance, filename):
    # Generate a unique filename using UUID
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('album/pictures/', new_filename)

class AlbumCover(models.Model):
    album = models.OneToOneField(
        Album,
        on_delete=models.CASCADE,
        related_name='cover',
        primary_key=True,
    )
    picture = models.ImageField(upload_to=custom_image_upload_path, default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)
