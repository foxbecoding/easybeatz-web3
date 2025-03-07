import pytest
from albums.models import Album


@pytest.fixture
def album(db, default_album):
    return default_album

@pytest.fixture
def album_cover(db, default_album_cover):
    return default_album_cover

