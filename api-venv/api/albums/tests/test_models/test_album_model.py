import pytest
from albums.models import Album, AlbumCover
from stations.tests.conftest import default_station

@pytest.fixture
def station(db, default_station):
    """Creates Station fixture"""
    return default_station

