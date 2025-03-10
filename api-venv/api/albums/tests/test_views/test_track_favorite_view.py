import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from albums.models import TrackFavorite
from users.tests.conftest import default_user
import logging

logger = logging.getLogger("albums")

@pytest.mark.django_db
class TestTrackFavoriteViewSet:

    @pytest.fixture
    def client(self):
        settings.SECURE_SSL_REDIRECT = False  # Disable automatic redirect to HTTPS
        return APIClient()

    @pytest.fixture
    def user(self, default_user):
        return default_user

    @pytest.fixture
    def track(self, default_track):
        return default_track

    @pytest.fixture
    def track_favorite(self, default_track_favorite):
        return default_track_favorite

    @pytest.mark.django_db
    def test_track_favorite_create_view(self, client, track, user):
        client.force_authenticate(user=user)

        data = {"track": track.tid}
        url = reverse("track-favorite-list")
        response = client.post(url, data)

        assert response.status_code == 201
        assert TrackFavorite.objects.all().count() > 0
        assert response.data.get("message") == "Track added to favorites"
        assert response.data.get("data") == str(track.tid)


    @pytest.mark.django_db
    def test_unauthenticated_cannot_favorite_track(self, client, track):
        data = {"track": track.tid}
        url = reverse("track-favorite-list")
        response = client.post(url, data)

        assert response.status_code == 401

    @pytest.mark.django_db
    def test_track_favorite_create_view_invalid_track_error(self, client, track, user):
        client.force_authenticate(user=user)

        data = {"track": "wrong_id"}
        url = reverse("track-favorite-list")
        response = client.post(url, data)

        assert response.status_code == 400
        assert response.data.get("message") == "Track not found"
        assert response.data.get("data") is None

    @pytest.mark.django_db
    def test_track_favorite_create_view_serializer_error(self, client, track_favorite, track, user):
        client.force_authenticate(user=user)

        data = {"track": track.tid}
        url = reverse("track-favorite-list")
        response = client.post(url, data)

        assert response.status_code == 400
        assert response.data.get("message") == "Something went wrong, please try again"
        assert response.data.get("data") is not None


    @pytest.mark.django_db
    def test_track_favorite_delete_view(self, client, track, track_favorite, user):
        client.force_authenticate(user=user)

        url = reverse("track-favorite-detail", kwargs={"pk": str(track.tid)})
        response = client.delete(url)

        assert response.status_code == 202
        assert TrackFavorite.objects.all().count() == 0
        assert response.data.get("message") == "Track removed from favorites"
        assert response.data.get("data") == str(track.tid)

    @pytest.mark.django_db
    def test_track_favorite_delete_view_invalid_track_error(self, client, track_favorite, user):
        client.force_authenticate(user=user)

        url = reverse("track-favorite-detail", kwargs={"pk": "wrong_id"})
        response = client.delete(url)

        assert response.status_code == 400
        assert response.data.get("message") == "Track not found"
        assert response.data.get("data") is None

    @pytest.mark.django_db
    def test_unauthenticated_cannot_unfavorite_track(self, client, track):
        data = {"track": track.tid}
        url = reverse("track-favorite-detail", kwargs={"pk": None})
        response = client.delete(url, data)

        assert response.status_code == 401

