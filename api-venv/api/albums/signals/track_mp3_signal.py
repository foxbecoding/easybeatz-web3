from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import TrackMp3, TrackDisplay
from ..utils import process_audio  # Import helper function

@receiver(post_save, sender=TrackMp3)
def after_save(sender, instance: TrackMp3, created, **kwargs):
    if created:
        track_display = TrackDisplay(
            track=instance.track,
            audio=process_audio(instance),  # Call the helper function
        )
        track_display.save()
