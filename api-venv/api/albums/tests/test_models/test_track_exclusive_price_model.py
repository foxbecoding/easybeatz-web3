import pytest
from albums.models import TrackExclusivePrice

@pytest.fixture
def track(db, default_track):
    """Creates track fixture"""
    return default_track

