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
    """Test TrackWav creation"""
    track_wav = TrackWav.objects.create(
        track=track,
        audio=test_wav_file
    )
    
    assert track_wav is not None

@pytest.mark.django_db
def test_fixture_creates_track_wav(db, track_wav):
    """Test track_wav fixture"""
    assert track_wav is not None
