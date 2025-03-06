from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from stations.models import StationPicture
from users.tests.conftest import default_user
import logging
from PIL import Image
import io


logger = logging.getLogger("stations")

@pytest.mark.django_db
class TestStationPictureViewSet:
    @pytest.fixture
    def client(self):
        settings.SECURE_SSL_REDIRECT = False  # Disable automatic redirect to HTTPS
        return APIClient()

    @pytest.fixture
    def user(self, default_user):
        return default_user

