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
def genre(db, default_genre):
    """Creates genre fixture"""
    return default_genre

@pytest.fixture
def mood(db, default_mood):
    """Creates mood fixture"""
    return default_mood

@pytest.fixture
def test_mp3_file():
    """Creates a temporary MP3 file for testing."""
    with tempfile.NamedTemporaryFile(suffix="mp3", delete=False) as tmp_file:
        audio = AudioSegment.silent(duration=1000)  # 1 second of silence
        audio.export(tmp_file.name, format="mp3")  # Save as MP3 or WAV
        return tmp_file.name  # Return path of temp AUDIO file

@pytest.fixture
def test_wav_file():
    """Creates a temporary WAV file for testing."""
    with tempfile.NamedTemporaryFile(suffix="wav", delete=False) as tmp_file:
        audio = AudioSegment.silent(duration=1000)  # 1 second of silence
        audio.export(tmp_file.name, format="wav")  # Save as MP3 or WAV
        return tmp_file.name  # Return path of temp AUDIO file

@pytest.fixture
def test_img_file():
    """Creates a temporary Image file in-memory for testing."""
    image = Image.new("RGB", (100, 100), color="red")
    image_io = io.BytesIO()
    image.save(image_io, format="JPEG")
    image_io.seek(0)

    return SimpleUploadedFile(
        "test_image.jpg",
        image_io.getvalue(),
        content_type="image/jpeg"
    )

@pytest.fixture
def default_album(db, default_station):
    """Fixture to create a test album."""
    return Album.objects.create(
        station=default_station,
        title="Test Album",
        bio="This is a test album.",
    )

@pytest.fixture
def default_album_cover(db, default_album, test_img_file):
    """Create a test AlbumCover with an in-memory image"""
    return AlbumCover.objects.create(
        album=default_album,
        picture=test_img_file,
    )

@pytest.fixture
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
