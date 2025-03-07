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

