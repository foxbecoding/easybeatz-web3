import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from users.tests.conftest import default_user
from genres.tests.conftest import default_genre
from moods.tests.conftest import default_mood
from stations.tests.conftest import default_station
from albums.tests.conftest import default_album, default_track, default_track_price, default_track_exclusive_price
from carts.models import *
import logging

logger = logging.getLogger("carts")
@pytest.mark.django_db
class TestCartViewSet:

    @pytest.fixture
    def client(self):
        settings.SECURE_SSL_REDIRECT = False  # Disable automatic redirect to HTTPS
        return APIClient()

    @pytest.fixture
    def user(self, default_user):
        """Fixture to create a test user with a public key."""
        return default_user

    @pytest.fixture
    def station(self, default_station):
        return default_station

    @pytest.fixture
    def album(self, default_album):
        return default_album

    @pytest.fixture
    def track(self, default_track):
        return default_track

    @pytest.fixture
    def track_price(self, default_track_price):
        return default_track_price

    @pytest.fixture
    def track_exclusive_price(self, default_track_exclusive_price):
        return default_track_exclusive_price

    @pytest.fixture
    def genre(self, default_genre):
        return default_genre

    @pytest.fixture
    def mood(self, default_mood):
        return default_mood

    @pytest.fixture
    def cart(self, default_cart):
        return default_cart

    @pytest.fixture
    def cart_item(self, default_cart_item):
        return default_cart_item

    @pytest.fixture
    def cart_item_exclusive(self, default_cart_item_exclusive):
        return default_cart_item_exclusive

    @pytest.fixture
    def request_data_track_price(self, track):
        return {
            "tid": track.tid,
            "type": "TRACK_PRICE"
        }

    @pytest.fixture
    def request_data_track_exclusive_price(self, track):
        return {
            "tid": track.tid,
            "type": "TRACK_EXCLUSIVE_PRICE"
        } 

    @pytest.fixture
    def invalid_request_data_tid(self, track):
        return {
            "tid": "wrong_tid",
            "type": "TRACK_PRICE"
        }

    @pytest.fixture
    def invalid_request_data_type(self, track):
        return {
            "tid": track.tid,
            "type": "WRONG_TYPE"
        }


