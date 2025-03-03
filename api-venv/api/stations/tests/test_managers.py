import pytest
from django.apps import apps
from django.utils.timezone import now
from users.models import User
from users.tests.conftest import default_user
from stations.models import Station, StationPicture
from albums.models import Album, Track


@pytest.fixture
def album(db, station):
    """Fixture to create an album linked to a station."""
    return Album.objects.create(
        user=station.user,
        title="Test Album",
        aid="album123",
        bio="This is a test album."
    )


@pytest.fixture
def track(db, album):
    """Fixture to create a track linked to an album."""
    return Track.objects.create(
        album=album,
        title="Test Track",
        tid="track123",
        duration=120
    )


