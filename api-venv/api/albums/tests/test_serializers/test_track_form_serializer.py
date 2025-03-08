import pytest
from genres.tests.conftest import default_genre
from moods.tests.conftest import default_mood
from users.tests.conftest import default_user
from stations.tests.conftest import default_station
from albums.serializers import TrackFormSerializer

@pytest.fixture
def user(default_user):
    return default_user

@pytest.fixture
def station(default_station):
    return default_station

@pytest.fixture
def genre(default_genre):
    return default_genre

@pytest.fixture
def mood(default_mood):
    return default_mood

@pytest.fixture
def valid_data(genre, mood, test_mp3_file, test_wav_file, test_wav_file2, test_img_file):
    """Fixture for test request data"""

    return {
        "title": "Test Track",
        "genres": [genre.pk],
        "mood": mood.pk,
        "mp3": test_mp3_file,
        "wav": test_wav_file,
        "bpm": "120",
        "price": "100",
        "exclusive_price": "200",
        "collaborators": [],
        "stems": [{"name": "snare", "file": test_wav_file2}]
    }

@pytest.fixture
def serializer_context(valid_data):
    """Mock serializer context."""
    return {
        'index': 0,
        'track_data': valid_data
    }

# ---------------------- TESTS ----------------------

def test_valid_serializer(valid_data, serializer_context):
    """Test valid serializer data."""
    serializer = TrackFormSerializer(data=valid_data, context=serializer_context)
    assert serializer.is_valid()
    assert serializer.validated_data['title'] == valid_data['title']
    assert serializer.validated_data['price'] == valid_data['price']

def test_invalid_price(valid_data, serializer_context):
    """Test invalid price values."""
    invalid_data = valid_data.copy()
    invalid_data['price'] = 'abc'  # Non-numeric price

    serializer = TrackFormSerializer(data=invalid_data, context=serializer_context)
    assert not serializer.is_valid()
    assert 'track_0' in serializer.errors['price']

    invalid_data['price'] = '012'  # Leading zero
    serializer = TrackFormSerializer(data=invalid_data, context=serializer_context)
    assert not serializer.is_valid()

    invalid_data['price'] = '0'  # Zero value
    serializer = TrackFormSerializer(data=invalid_data, context=serializer_context)
    assert not serializer.is_valid()

def test_invalid_exclusive_price(valid_data, serializer_context):
    """Test invalid exclusive price values."""
    invalid_data = valid_data.copy()
    invalid_data['exclusive_price'] = 'abc'  # Non-numeric exclusive price

    serializer = TrackFormSerializer(data=invalid_data, context=serializer_context)
    assert not serializer.is_valid()

    invalid_data['exclusive_price'] = '012'  # Leading zero
    serializer = TrackFormSerializer(data=invalid_data, context=serializer_context)
    assert not serializer.is_valid()

    invalid_data['exclusive_price'] = '0'  # Zero value
    serializer = TrackFormSerializer(data=invalid_data, context=serializer_context)
    assert not serializer.is_valid()

