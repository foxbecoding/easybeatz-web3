import pytest
from albums.models import TrackWav
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def track(db, default_track):
    """Creates track fixture"""
    return default_track

@pytest.fixture
def track_wav(db, default_track_wav):
    """Creates track_wav fixture"""
    return default_track_wav

@pytest.mark.django_db
def test_track_wav_create(db, track, test_wav_file):
    """Creates a TrackWav instance with a test Wav file."""
    with open(test_wav_file, "rb") as wav:
        uploaded_audio = SimpleUploadedFile("test_display.wav", wav.read(), content_type="audio/wav")

    """Test TrackWav creation"""
    track_wav = TrackWav.objects.create(
        track=track,
        audio=uploaded_audio
    )
    
    assert track_wav is not None

