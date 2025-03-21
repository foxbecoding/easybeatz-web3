import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from albums.models import TrackExclusivePrice
from users.tests.conftest import default_user
from genres.tests.conftest import default_genre
from moods.tests.conftest import default_mood
from stations.tests.conftest import default_station
import logging

logger = logging.getLogger("albums")

@pytest.mark.django_db
class TestTrackExclusivePriceViewSet:

    @pytest.fixture
    def client(self):
        settings.SECURE_SSL_REDIRECT = False  # Disable automatic redirect to HTTPS
        return APIClient()

