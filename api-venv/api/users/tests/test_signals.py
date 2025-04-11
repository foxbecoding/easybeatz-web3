import pytest
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from users.models import UserLogin
from users.signals.user_login_signal import web3_login_done
from carts.tests.conftest import default_cart, default_cart_item
from genres.tests.conftest import default_genre
from moods.tests.conftest import default_mood
from stations.tests.conftest import default_station
from albums.tests.conftest import default_album, default_track, default_track_price, default_track_exclusive_price

@pytest.fixture
def user(db, default_user):
    """Fixture to create a test user with a public key."""
    return default_user

@pytest.fixture
def station(db, default_station):
    return default_station

@pytest.fixture
def album(db, default_album):
    return default_album

@pytest.mark.django_db
def test_web3_login_done_handler(default_user):
    """Test that the web3_login_done signal creates a UserLogin record."""

    # Ensure no UserLogin records exist before the signal
    assert UserLogin.objects.filter(user=default_user).count() == 0

    # Send the web3_login_done signal
    web3_login_done.send(sender=None, user=default_user)

    # Verify that a UserLogin record is created
    assert UserLogin.objects.filter(user=default_user).count() == 1
