import pytest
from albums.models import TrackFavorite
from users.tests.conftest import User

@pytest.fixture
def track(default_track):
    return default_track

