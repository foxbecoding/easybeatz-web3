import pytest
from django.apps import apps
from django.utils.timezone import now
from users.models import User
from users.tests.conftest import default_user
from albums.tests.conftest import default_album, default_track
from genres.tests.conftest import default_genre
from moods.tests.conftest import default_mood
from stations.models import Station, StationPicture
from stations.tests.factories import StationFactory


@pytest.mark.django_db
def test_with_albums_and_relations_single(db, default_station, default_user, default_genre, default_mood, default_album, default_track):
    """Test that `with_albums_and_relations` correctly fetches a single station with related data."""
     
    station_with_relations = Station.stations.with_albums_and_relations(default_user.pubkey)

    assert station_with_relations is not None
    assert station_with_relations.name == "Test Station"
    assert station_with_relations.user.pubkey == default_user.pubkey

    # Ensure albums are prefetched
    assert station_with_relations.albums.count() == 1
    assert station_with_relations.albums.first().title == "Test Album"

    # Ensure tracks are prefetched in the album
    assert station_with_relations.albums.first().tracks.count() == 1
    assert station_with_relations.albums.first().tracks.first().title == "Test Track"
