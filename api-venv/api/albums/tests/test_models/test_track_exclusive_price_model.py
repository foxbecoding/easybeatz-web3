import pytest
from albums.models import TrackExclusivePrice

@pytest.fixture
def track(db, default_track):
    """Creates track fixture"""
    return default_track

@pytest.fixture
def track_exclusive_price(db, default_track_exclusive_price):
    """Creates track_exclusive_price fixture"""
    return default_track_exclusive_price

