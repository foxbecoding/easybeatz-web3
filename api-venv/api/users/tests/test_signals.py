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

@pytest.fixture
def track(db, default_track):
    return default_track

@pytest.fixture
def track_price(db, default_track_price):
    return default_track_price

@pytest.fixture
def track_exclusive_price(db, default_track_exclusive_price):
    return default_track_exclusive_price

@pytest.fixture
def genre(db, default_genre):
    return default_genre

@pytest.fixture
def mood(db, default_mood):
    return default_mood

@pytest.fixture
def cart(db, default_cart):
    return default_cart

@pytest.fixture
def cart_item(db, default_cart_item):
    return default_cart_item


@pytest.mark.django_db
def test_web3_login_done_handler(user):
    """Test that the web3_login_done signal creates a UserLogin record.""" 

    # Ensure no UserLogin records exist before the signal
    assert UserLogin.objects.filter(user=user).count() == 0

    # Send the web3_login_done signal
    web3_login_done.send(sender=None, user=user)

    # Verify that a UserLogin record is created
    assert UserLogin.objects.filter(user=user).count() == 1

@pytest.mark.django_db
def test_web3_login_done_with_cart_handler(user, station, cart, album, track, track_price, track_exclusive_price, genre, mood, cart_item):
    """Test that the web3_login_done signal creates a UserLogin record.""" 

    factory = RequestFactory()
    request = factory.get("/")  # or .post() if needed

    # Set the cookie manually
    request.COOKIES["cart_id"] = cart.cart_id 

    # Ensure no UserLogin records exist before the signal
    assert UserLogin.objects.filter(user=user).count() == 0

    # Send the web3_login_done signal
    web3_login_done.send(sender=None, user=user, request=request)

    # Verify that a UserLogin record is created
    assert UserLogin.objects.filter(user=user).count() == 1

@pytest.mark.django_db
def test_web3_login_done_without_cart_handler(user, station, cart, album, track, track_price, track_exclusive_price, genre, mood, cart_item):
    """Test that the web3_login_done signal creates a UserLogin record.""" 

    factory = RequestFactory()
    request = factory.get("/")  # or .post() if needed

    # Set the cookie manually
    request.COOKIES["cart_id"] = "cart.cart_id"

    # Ensure no UserLogin records exist before the signal
    assert UserLogin.objects.filter(user=user).count() == 0

    # Send the web3_login_done signal
    web3_login_done.send(sender=None, user=user, request=request)

    # Verify that a UserLogin record is created
    assert UserLogin.objects.filter(user=user).count() == 1
