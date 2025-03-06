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

    @pytest.fixture
    def station(self, default_station):
        return default_station

    @pytest.fixture
    def station_picture(self, default_station_picture):
        return default_station_picture

    def test_authenticated_user_can_upload_picture(self, client, user, station):
        client.force_authenticate(user=user)
        image = Image.new("RGB", (100, 100), color="red")
        image_io = io.BytesIO()
        image.save(image_io, format="JPEG")
        image_io.seek(0)
        uploaded_image =SimpleUploadedFile(
            "test_image.jpg",
            image_io.getvalue(),
            content_type="image/jpeg"
        )

        data = {"picture": uploaded_image}

        url = reverse("station-picture-upload")  # Update with your actual URL name
        response = client.post(url, data, format="multipart")
        
        assert response.status_code == status.HTTP_200_OK
        assert "Picture uploaded successfully" in response.data
        assert StationPicture.objects.filter(station=station).exists()

    def test_authenticated_user_can_update_existing_picture(self, client, user, station_picture):
        client.force_authenticate(user=user)
        image = Image.new("RGB", (100, 100), color="red")
        image_io = io.BytesIO()
        image.save(image_io, format="JPEG")
        image_io.seek(0)
        uploaded_image =SimpleUploadedFile(
            "new.jpg",
            image_io.getvalue(),
            content_type="image/jpeg"
        )
        data = {"picture": uploaded_image}

        url = reverse("station-picture-upload")  # Update with your actual URL name
        response = client.post(url, data, format="multipart")

        assert response.status_code == status.HTTP_200_OK

