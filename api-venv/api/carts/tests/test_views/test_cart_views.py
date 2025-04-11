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

