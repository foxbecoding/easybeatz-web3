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

