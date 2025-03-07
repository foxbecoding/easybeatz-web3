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

@pytest.mark.django_db
def test_track_price_create(db, track):
    """Test TrackPrice creation"""
    track_price = TrackPrice.objects.create(
        track=track,
        value=36
    )
    
    assert track_price is not None
    assert track_price.value == 36

