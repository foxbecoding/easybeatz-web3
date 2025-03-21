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

    @pytest.fixture
    def user(self, default_user):
        return default_user

    @pytest.fixture
    def album(self, default_album):
        return default_album

    @pytest.fixture
    def track(self, default_track):
        return default_track

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
    def test_track_exclusive_price_create_view(self, client, user, station, album, track, track_price, mood, genre):
        client.force_authenticate(user=user)
        data = {"value": 500}
        url = reverse("track-exclusive-price-detail", kwargs={"pk": track.tid})
        response = client.put(url, data)
       
        logger.info(response.data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("message") == "Exclusive price added successfully"
        assert response.data.get("data") is None

        qs = TrackExclusivePrice.objects.get(track__tid=track.tid)
        assert qs.value == 500

    @pytest.mark.django_db
    def test_track_exclusive_price_create_view_error(self, db, client, user, station, album, track, track_price, mood, genre):
        client.force_authenticate(user=user)
        data = {"value": .50}
        url = reverse("track-exclusive-price-detail", kwargs={"pk": track.tid})
        response = client.put(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("message") == "Failed to add exclusive price"
        assert response.data.get("data") is not None

