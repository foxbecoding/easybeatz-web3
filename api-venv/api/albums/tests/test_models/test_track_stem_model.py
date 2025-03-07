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

