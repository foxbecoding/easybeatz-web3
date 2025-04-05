import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from users.tests.conftest import default_user
from genres.tests.conftest import default_genre
from moods.tests.conftest import default_mood
from stations.tests.conftest import default_station, default_station_picture
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

    @pytest.fixture
    def album_cover(self, default_album_cover):
        return default_album_cover

    @pytest.fixture
    def track(self, default_track):
        return default_track

    @pytest.fixture
    def track_display(self, default_track_display):
        return default_track_display
    
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
    def station(self, default_station):
        return default_station

    @pytest.mark.django_db
    def test_track_update_view(self, client, user, station, album, track, mood, genre):
        client.force_authenticate(user=user)
        data = {"title": "New title", "bpm": 135, "genres": [genre.pk], "mood": mood.pk}
        url = reverse("track-detail", kwargs={"pk": track.tid})
        response = client.put(url, data)
        
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.data.get("message") == "Track updated successfully"
        assert response.data.get("data") is None

        track.refresh_from_db()
        assert track.title == "New title"
        assert track.bpm == "135"

    @pytest.mark.django_db
    def test_track_update_view_error(self, db, client, user, station, album, track, mood, genre):
        client.force_authenticate(user=user)
        data = {"bpm": 135, "genres": [genre.pk], "mood": mood.pk}
        url = reverse("track-detail", kwargs={"pk": track.tid})
        response = client.put(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("message") == "Failed to update track"
        assert response.data.get("data") is not None

    @pytest.mark.django_db 
    def test_non_track_owner_cannot_update(self, db, client, user, station, album, track, genre, mood):
        client.force_authenticate(user=user)
        data = {"bpm": 135, "genres": [genre.pk], "mood": mood.pk}
        url = reverse("track-detail", kwargs={"pk": "wrong_tid"})
        response = client.put(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_unauthenticated_cannot_update_track_view(self, db, client):
        url = reverse("track-detail", kwargs={"pk": None})
        response = client.put(url, None)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
