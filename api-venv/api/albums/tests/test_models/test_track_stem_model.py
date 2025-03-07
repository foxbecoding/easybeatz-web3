import pytest
from albums.models import TrackStem
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def track(db, default_track):
    """Creates track fixture"""
    return default_track

@pytest.fixture
def track_stem(db, default_track_stem):
    """Creates track_stem fixture"""
    return default_track_stem

@pytest.mark.django_db
def test_track_stem_create(db, track, test_wav_file):
    """Creates a TrackStem instance with a test Wav file."""
    with open(test_wav_file, "rb") as wav:
        uploaded_audio = SimpleUploadedFile("test_display.wav", wav.read(), content_type="audio/wav")

    """Test TrackStem creation"""
    track_stem = TrackStem.objects.create(
        track=track,
        name="snare",
        audio=uploaded_audio
    )
    
    assert track_stem is not None

