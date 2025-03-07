import pytest
from albums.models import Album


@pytest.fixture
def album(db, default_album):
    return default_album

@pytest.fixture
def album_cover(db, default_album_cover):
    return default_album_cover

@pytest.fixture
def track(db, default_track):
    return default_track

@pytest.fixture
def track_price(db, default_track_price):
    return default_track_price

@pytest.fixture
def track_exclusive_price(db, default_track_exclusive_price):
    return default_track_exclusive_price

@pytest.fixture
def track_display(db, default_track_display):
    return default_track_display

@pytest.fixture
def track_mp3(db, default_track_mp3):
    return default_track_mp3

