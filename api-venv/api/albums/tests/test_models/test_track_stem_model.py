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
    """Test TrackStem creation"""
    track_stem = TrackStem.objects.create(
        track=track,
        name="snare",
        audio=test_wav_file
    )
    
    assert track_stem is not None

@pytest.mark.django_db
def test_fixture_creates_track_stem(db, track_stem):
    """Test track_stem fixture"""
    assert track_stem is not None
