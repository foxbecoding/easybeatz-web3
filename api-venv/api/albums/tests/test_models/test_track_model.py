import pytest
from albums.models import Track
from genres.tests.conftest import default_genre
from moods.tests.conftest import default_mood

@pytest.fixture
def genre(db, default_genre):
    """Creates genre fixture"""
    return default_genre

@pytest.fixture
def mood(db, default_mood):
    """Creates mood fixture"""
    return default_mood

@pytest.fixture
def album(db, default_album):
    """Creates album fixture"""
    return default_album

@pytest.fixture
def track(db, default_track):
    """Creates track fixture"""
    return default_track

@pytest.fixture
def track_with_an_hour(db, default_track_with_an_hour):
    """Creates track with an hour fixture"""
    return default_track_with_an_hour

@pytest.fixture
def track_display(db, default_track_display):
    """Creates track_display fixture"""
    return default_track_display

