import uuid, os
from django.db import models
from .track import Track

def audio_file_path(instance, filename):
    """Generate a unique file path for new audio file using UUID."""
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('track/wav/', new_filename)

class TrackWav(models.Model):
    track = models.OneToOneField(
        Track,
        on_delete=models.CASCADE,
        related_name='wav',
        primary_key=True,
    )
    audio = models.FileField(upload_to=audio_file_path, default="")
    provided_by_eb = models.BooleanField(blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)
    
    objects = models.Manager()
