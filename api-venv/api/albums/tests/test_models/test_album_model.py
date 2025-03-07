import pytest
from albums.models import Album, AlbumCover
from stations.tests.conftest import default_station

@pytest.fixture
def station(db, default_station):
    """Creates Station fixture"""
    return default_station

@pytest.fixture
def album(db, default_album):
    """Creates Album fixture"""
    return default_album

@pytest.fixture
def album_cover(db, default_album_cover):
    """Creates AlbumCover fixture"""
    return default_album_cover

