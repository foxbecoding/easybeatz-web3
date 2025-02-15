import io
from pydub import AudioSegment
from django.core.files.base import ContentFile
from .models import TrackMp3
from .signals.update_track_duration_signal import update_track_duration

def process_audio(track_mp3: TrackMp3) -> ContentFile:
    """Processes the MP3 file and returns a ContentFile object."""
    track_pk = track_mp3.track.pk
    track_audio = track_mp3.audio

    # Process MP3 file (fade-in and fade-out effect)
    mp3 = AudioSegment.from_mp3(track_audio)
    mp3 = mp3.fade_in(5000).fade_out(5000)
    duration = mp3.duration_seconds
    
    # Convert to a BytesIO buffer
    buffer = io.BytesIO()
    mp3.export(buffer, format="mp3")
    buffer.seek(0)

    update_track_duration.send(sender=None, track_pk=track_pk, duration=duration)

    # Return ContentFile with a meaningful name
    return ContentFile(buffer.read(), name=f"track_{track_pk}.mp3")
