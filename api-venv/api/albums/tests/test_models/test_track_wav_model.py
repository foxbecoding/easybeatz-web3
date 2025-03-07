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

