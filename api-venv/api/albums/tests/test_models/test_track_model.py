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

@pytest.mark.django_db
def test_track_create(db, album, genre, mood):
    """Test Track creation"""
    track = Track.objects.create(
        album=album,
        mood=mood,
        title="Test Track",
        bpm="120",
        duration=180,  # 3 minutes
        order_no=1,
    )
    track.genres.add(genre) 
    
    assert track is not None

@pytest.mark.django_db
def test_track_display_url(db, track, track_display):
    """Test Track display url property"""
    assert track.display_url is not None

@pytest.mark.django_db
def test_track_formatted_duration(db, track, track_display):
    """Test Track formatted_duration property"""

    assert track.formatted_duration is not None
    assert track.formatted_duration == "3:00"

