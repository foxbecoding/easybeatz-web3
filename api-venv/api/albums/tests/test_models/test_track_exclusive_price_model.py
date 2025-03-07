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

@pytest.mark.django_db
def test_track_exclusive_price_create(db, track):
    """Test TrackExclusivePrice creation"""
    track_exclusive_price = TrackExclusivePrice.objects.create(
        track=track,
        value=360
    )
    
    assert track_exclusive_price is not None
    assert track_exclusive_price.value == 360

