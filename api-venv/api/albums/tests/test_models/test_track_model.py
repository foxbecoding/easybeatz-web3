import pytest
from albums.models import Track
from genres.tests.conftest import default_genre
from moods.tests.conftest import default_mood

@pytest.fixture
def genre(db, default_genre):
    """Creates genre fixture"""
    return default_genre

