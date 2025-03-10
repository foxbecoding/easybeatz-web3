import pytest
from albums.models import TrackFavorite
from users.tests.conftest import User

@pytest.fixture
def track(default_track):
    return default_track

@pytest.fixture
def user(default_user):
    return default_user

@pytest.mark.django_db
def test_track_favorite_create(track, user):
    instance = TrackFavorite.objects.create(track=track, user=user)
    instance.save()

    assert TrackFavorite.objects.all().count() > 0

@pytest.mark.django_db
def test_track_favorite_str(track, user):
    instance = TrackFavorite.objects.create(track=track, user=user)
    instance.save()

    assert str(instance) == f"{user} - {track}"
