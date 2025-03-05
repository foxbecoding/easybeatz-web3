
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from stations.models import Station
from users.tests.conftest import default_user
from albums.tests.conftest import default_album, default_album_cover, default_track
from django.conf import settings
import logging

logger = logging.getLogger("stations")
@pytest.mark.django_db
class TestStationViewSet:
    
    @pytest.fixture
    def client(self):
        settings.SECURE_SSL_REDIRECT = False  # Disable automatic redirect to HTTPS
        return APIClient()

    @pytest.fixture
    def user(self, default_user):
        """Fixture to create a test user with a public key."""
        return default_user

    @pytest.fixture
    def station(self, db, default_station):
        """Fixture to create a test station."""
        return default_station

    @pytest.fixture
    def station_picture(self, db, default_station_picture):
        """Fixture to create a test station."""
        return default_station_picture

