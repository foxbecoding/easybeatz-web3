import pytest
from django.apps import apps
from django.utils.timezone import now
from users.models import User
from users.tests.conftest import default_user
from albums.tests.conftest import default_album, default_track
from stations.models import Station, StationPicture
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


@pytest.mark.django_db
def test_with_albums_and_relations_single(default_station, album, track):
    """Test that `with_albums_and_relations` correctly fetches a single station with related data."""
    station_with_relations = Station.stations.with_albums_and_relations("test_pubkey")

    assert station_with_relations is not None
    assert station_with_relations.name == "Test Station"
    assert station_with_relations.user.pubkey == "test_pubkey"
    
    # Ensure albums are prefetched
    assert station_with_relations.albums.count() == 1
    assert station_with_relations.albums.first().title == "Test Album"

    # Ensure tracks are prefetched in the album
    assert station_with_relations.albums.first().tracks.count() == 1
    assert station_with_relations.albums.first().tracks.first().title == "Test Track"


@pytest.mark.django_db
def test_with_albums_and_relations_multiple(default_station, album, track):
    """Test that `with_albums_and_relations` correctly fetches multiple stations."""
    user2 = User.objects.create(email="test2@example.com", password="password", pubkey="test_pubkey2")
    station2 = Station.objects.create(user=user2, name="Another Station", handle="another_handle", email="test2@example.com")

    stations = Station.stations.with_albums_and_relations(["test_pubkey", "test_pubkey2"])

    assert stations.count() == 2
    assert set(stations.values_list("name", flat=True)) == {"Test Station", "Another Station"}
