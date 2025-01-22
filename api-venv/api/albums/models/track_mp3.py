import uuid, os
from django.db import models
from .track import Track

def audio_file_path(instance, filename):
    """Generate a unique file path for new audio file using UUID."""
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('track/mp3/', new_filename)

class TrackMp3(models.Model):
    track = models.OneToOneField(
        Track,
        on_delete=models.CASCADE,
        related_name='mp3',
        primary_key=True,
    )
    audio = models.FileField(upload_to=audio_file_path, default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)
