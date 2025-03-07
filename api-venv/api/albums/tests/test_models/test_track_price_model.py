import pytest
from albums.models import TrackPrice

@pytest.fixture
def track(db, default_track):
    """Creates track fixture"""
    return default_track

