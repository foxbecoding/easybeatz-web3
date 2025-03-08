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
        audio.export(tmp_file.name, format="mp3")  # Save as MP3
        with open(tmp_file.name, "rb") as mp3:
            uploaded_audio = SimpleUploadedFile("test_mp3.mp3", mp3.read(), content_type="audio/mp3")
            return uploaded_audio  # Return audio file

@pytest.fixture
def test_wav_file():
    """Creates a temporary WAV file for testing."""
    with tempfile.NamedTemporaryFile(suffix="wav", delete=False) as tmp_file:
        audio = AudioSegment.silent(duration=1000)  # 1 second of silence
        audio.export(tmp_file.name, format="wav")  # Save WAV
        with open(tmp_file.name, "rb") as wav:
            uploaded_audio = SimpleUploadedFile("test_wav.wav", wav.read(), content_type="audio/wav")
            return uploaded_audio

@pytest.fixture
def test_wav_file2():
    """Creates a temporary WAV file for testing."""
    with tempfile.NamedTemporaryFile(suffix="wav", delete=False) as tmp_file:
        audio = AudioSegment.silent(duration=1000)  # 1 second of silence
        audio.export(tmp_file.name, format="wav")  # Save WAV
        with open(tmp_file.name, "rb") as wav:
            uploaded_audio = SimpleUploadedFile("test_wav2.wav", wav.read(), content_type="audio/wav")
            return uploaded_audio

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
def default_track(db, default_album, genre, mood):
    """Fixture to create a test track."""
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

@pytest.fixture
def default_track_with_an_hour(db, default_album, genre, mood):
    """Fixture to create a test track."""
    track = Track.objects.create(
        album=default_album,
        mood=mood,
        title="Test Track",
        bpm="120",
        duration=3600,  # 3 minutes
        order_no=1,
    )
    track.genres.add(genre)  # Add the genre to ManyToManyField
    return track

@pytest.fixture
def default_track_price(db, default_track):
    """Fixture to create a test TrackPrice"""
    
    return TrackPrice.objects.create(track=default_track, value=36)

@pytest.fixture
def default_track_exclusive_price(db, default_track):
    """Fixture to create a test TrackExclusivePrice"""
   
    return TrackExclusivePrice.objects.create(track=default_track, value=369)

@pytest.fixture
def default_track_display(db, default_track, test_mp3_file):
    """Creates a TrackMp3 instance with a test MP3 file."""
    return TrackDisplay.objects.create(track=default_track, audio=test_mp3_file)

@pytest.fixture
def default_track_mp3(db, default_track, test_mp3_file):
    """Creates a TrackMp3 instance with a test MP3 file."""
    return TrackMp3.objects.create(track=default_track, audio=test_mp3_file)

@pytest.fixture
def default_track_wav(db, default_track, test_wav_file):
    """Creates a TrackWav instance with a test WAV file."""
    return TrackWav.objects.create(track=default_track, audio=test_wav_file)

@pytest.fixture
def default_track_stem(db, default_track, test_wav_file):
    """Creates a TrackWav instance with a test WAV file."""
    with open(test_wav_file, "rb") as wav:
        uploaded_audio = SimpleUploadedFile("test_stem.wav", wav.read(), content_type="audio/wav")

    return TrackStem.objects.create(track=default_track, name="test stem", audio=uploaded_audio)
