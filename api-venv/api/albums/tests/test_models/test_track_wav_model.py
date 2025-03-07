import pytest
from albums.models import TrackWav
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def track(db, default_track):
    """Creates track fixture"""
    return default_track

