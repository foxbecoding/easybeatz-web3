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

@pytest.fixture
def default_track(db, default_album):
    """Fixture to create a test track."""
    genre = Genre.objects.create(name="Test Genre")
    mood = Mood.objects.create(name="Test Mood")
    track = Track.objects.create(
        album=default_album,
        mood=mood,
        title="Test Track",
        bpm="120",
        duration=180,  # 3 minutes
        order_no=1,
    )
    track.genres.add(genre)  # Add the genre to ManyToManyField
    return track
