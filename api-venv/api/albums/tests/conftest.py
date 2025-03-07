import pytest
from stations.tests.conftest import default_station
from users.tests.conftest import default_user
from albums.models import Album, AlbumCover, Track, TrackDisplay, TrackMp3, TrackWav, TrackStem, TrackPrice, TrackExclusivePrice, TrackCollaborator
from genres.tests.conftest import default_genre
from moods.tests.conftest import default_mood
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from pydub import AudioSegment
import io
import tempfile

@pytest.fixture
def default_album(db, default_station):
    """Fixture to create a test album."""
    return Album.objects.create(
        station=default_station,
        title="Test Album",
        bio="This is a test album.",
    )

@pytest.fixture
def default_album_cover(db, default_album):
    """Create a test AlbumCover with an in-memory image"""
    # Create an in-memory image
    image = Image.new("RGB", (100, 100), color="red")
    image_io = io.BytesIO()
    image.save(image_io, format="JPEG")
    image_io.seek(0)

    uploaded_image = SimpleUploadedFile(
        "test_image.jpg",
        image_io.getvalue(),
        content_type="image/jpeg"
    )

    return AlbumCover.objects.create(
        album=default_album,
        picture=uploaded_image,
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
