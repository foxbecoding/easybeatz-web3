import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from albums.models import Album, Track
from stations.tests.conftest import default_station, default_station_picture
from users.tests.conftest import default_user
import logging

logger = logging.getLogger("albums")
@pytest.mark.django_db
class TestAlbumCoverViewSet:

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

