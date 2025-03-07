import pytest
from albums.models import TrackMp3
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def track(db, default_track):
    """Creates track fixture"""
    return default_track

@pytest.fixture
def track_mp3(db, default_track_mp3):
    """Creates track_mp3 fixture"""
    return default_track_mp3

@pytest.mark.django_db
def test_track_mp3_create(db, track, test_mp3_file):
    """Creates a TrackMp3 instance with a test MP3 file."""
    with open(test_mp3_file, "rb") as mp3:
        uploaded_audio = SimpleUploadedFile("test_display.mp3", mp3.read(), content_type="audio/mp3")

    """Test TrackMp3 creation"""
    track_mp3 = TrackMp3.objects.create(
        track=track,
        audio=uploaded_audio
    )
    
    assert track_mp3 is not None

