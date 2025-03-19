import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from users.tests.conftest import default_user
from genres.tests.conftest import default_genre
from moods.tests.conftest import default_mood
from stations.tests.conftest import default_station
import logging

logger = logging.getLogger("albums")

@pytest.mark.django_db
class TestTrackViewSet:

    @pytest.fixture
    def client(self):
        settings.SECURE_SSL_REDIRECT = False  # Disable automatic redirect to HTTPS
        return APIClient()

    @pytest.fixture
    def user(self, default_user):
        return default_user

    @pytest.fixture
    def album(self, default_album):
        return default_album

