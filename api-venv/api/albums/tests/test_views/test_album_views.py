import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from albums.models import Album, Track, TrackStem, TrackExclusivePrice
from genres.tests.conftest import default_genre
from moods.tests.conftest import default_mood
from stations.tests.conftest import default_station, default_station_picture
from users.tests.conftest import default_user
import logging

logger = logging.getLogger("albums")
@pytest.mark.django_db
class TestAlbumViewSet:

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
        return default_station_picture

    @pytest.fixture
    def genre(self, db, default_genre):
        """Fixture to create genre"""
        return default_genre
