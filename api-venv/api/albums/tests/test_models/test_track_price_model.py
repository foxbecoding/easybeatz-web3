import pytest
from albums.models import TrackPrice

@pytest.fixture
def track(db, default_track):
    """Creates track fixture"""
    return default_track

@pytest.fixture
def track_price(db, default_track_price):
    """Creates track_price fixture"""
    return default_track_price

