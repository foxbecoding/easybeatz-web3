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

    @pytest.fixture
    def album(self, db, default_album):
        return default_album

    @pytest.fixture
    def album_cover(self, db, default_album_cover):
        return default_album_cover
    
    @pytest.mark.django_db
    def test_album_cover_update_view(self, db, client, user, station, album, album_cover, test_img_file2):
        client.force_authenticate(user=user)
        url = reverse("album-cover-detail", kwargs={"pk": album.aid})
        updated_data = {"picture": test_img_file2}
        response = client.put(url, updated_data, format="multipart")

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.data.get("message") == "Album cover updated successfully"
        assert response.data.get("data") is None

    @pytest.mark.django_db
    def test_album_cover_update_view_error(self, db, client, user, station, album, album_cover):
        client.force_authenticate(user=user)
        url = reverse("album-cover-detail", kwargs={"pk": album.aid})
        updated_data = {"picture": ""}
        response = client.put(url, updated_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("message") == "Failed to update album cover"
        assert response.data.get("data") is not None

