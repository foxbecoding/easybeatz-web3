import pytest
from stations.tests.conftest import default_station
from albums.models import Album, Track
from genres.models import Genre
from moods.models import Mood

@pytest.fixture
def default_album(db, default_station):
    """Fixture to create a test album."""
    return Album.objects.create(
        station=default_station,
        title="Test Album",
        bio="This is a test album.",
    )

