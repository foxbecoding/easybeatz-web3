from django.dispatch import receiver, Signal
from ..models import Track

update_track_duration = Signal()

@receiver(update_track_duration)
def update_track_duration_handler(sender, track_pk, duration, **kwargs):
    track: Track = Track.objects.get(pk=track_pk)
    track.duration = duration
    track.save()
