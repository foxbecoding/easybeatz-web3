import pytest
from albums.models import Album, AlbumCover
from stations.tests.conftest import default_station

@pytest.fixture
def station(db, default_station):
    """Creates Station fixture"""
    return default_station

@pytest.fixture
def album(db, default_album):
    """Creates Album fixture"""
    return default_album

@pytest.fixture
def album_cover(db, default_album_cover):
    """Creates AlbumCover fixture"""
    return default_album_cover

@pytest.fixture
def track(db, default_track):
    """Creates Track fixture"""
    return default_track

@pytest.mark.django_db
def test_album_create(db, station):
    """Test Album creation"""
    album = Album.objects.create(
        station=station,
        title="Test Album",
        bio="This is a test album.",
    )

    assert album.pk is not None

@pytest.mark.django_db
def test_album_str_returns_pk(db, station, album):
    """Test Album return str"""
    assert str(album) == str(album.pk)

@pytest.mark.django_db
def test_album_uploaded_at(db, album):
    """Test Album uploaded_at property"""
    assert album.uploaded_at is not None

