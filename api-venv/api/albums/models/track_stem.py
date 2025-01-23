import uuid, os
from django.db import models
from .track import Track

def audio_file_path(instance, filename):
    """Generate a unique file path for new audio file using UUID."""
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('track/stems/', new_filename)

class TrackStem(models.Model):
    track = models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        related_name='stems',
    )
    name = models.CharField(max_length=120, default="")
    audio = models.FileField(upload_to=audio_file_path, default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)
