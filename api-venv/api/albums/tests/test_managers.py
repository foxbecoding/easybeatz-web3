import pytest
from albums.models import Album


@pytest.fixture
def album(db, default_album):
    return default_album

