import uuid, os
from django.db import models
from .track import Track

def audio_file_path(instance, filename):
    """Generate a unique file path for new audio file using UUID."""
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('track/display/', new_filename)

class TrackDisplay(models.Model):
    track = models.OneToOneField(
        Track,
        on_delete=models.CASCADE,
        related_name='display',
        primary_key=True,
    )
    audio = models.FileField(upload_to=audio_file_path, default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)
    
    objects = models.Manager()

    @property
    def display_url(self):
        return self.audio.url
