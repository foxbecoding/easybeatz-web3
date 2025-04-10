import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from stations.models import Station
from users.tests.conftest import default_user
from albums.tests.conftest import default_album, default_album_cover, default_track, test_img_file
from genres.tests.conftest import default_genre
from moods.tests.conftest import default_mood
from django.conf import settings
import logging

logger = logging.getLogger("stations")
@pytest.mark.django_db
class TestStationViewSet:
    
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
        """Fixture to create a test station."""
        return default_station_picture

    @pytest.fixture
    def album(self, db, default_album):
        """Fixture to create a test album"""
        return default_album

    @pytest.fixture
    def album_cover(self, db, default_album_cover):
        """Fixture to create a test album_cover"""
        return default_album_cover
    
    @pytest.fixture
    def track(self, db, default_track):
        """Fixture to create a test track"""
        return default_track

    def test_create_station(self, client, user):
        """Test creating a new station."""
        client.force_authenticate(user=user)
        url = reverse("station-list")  # Assuming the route name is station-list (ViewSets use `basename`)
        data = {"name": "My Station", "handle": "testhandle", "email": "test@email.com", "description": ""}

        response = client.post(url, data, format="json")
        
        assert response.status_code == 201
        assert response.data.get("message") == "Station created successfully!"
        assert response.data.get("data") is None
        assert Station.objects.filter(name="My Station").exists()

    def test_create_station_error(self, client, user):
        """Test creating a new station."""
        client.force_authenticate(user=user)
        url = reverse("station-list")  # Assuming the route name is station-list (ViewSets use `basename`)
        invalid_data = {"handle": "__dsi-="}

        response = client.post(url, invalid_data, format="json")
        
        assert response.status_code == 400
        assert response.data.get("message") == "Failed to create station"
        assert response.data.get("data") is not None

    def test_retrieve_station(self, client, user, station):
        """Test retrieving a station with correct user."""
        client.force_authenticate(user=user)
        url = reverse("station-detail", kwargs={"pk": user.pubkey})

        response = client.get(url)

        assert response.status_code == 200
        assert response.data.get("message") is None
        assert response.data.get("data") is not None

    def test_update_station(self, client, user, station):
        """Test updating a station."""
        client.force_authenticate(user=user)
        url = reverse("station-detail", kwargs={"pk": user.pubkey})
        data = {"name": "Updated Station", "handle": "testhandle", "email": "test@email.com", "description": ""}

        response = client.put(url, data, format="json")
        assert response.status_code == 200
        assert response.data.get("message") == "Station updated"
        assert response.data.get("data") is not None
        station.refresh_from_db()
        assert station.name == "Updated Station"

    def test_update_station_error(self, client, user, station):
        """Test updating a station."""
        client.force_authenticate(user=user)
        url = reverse("station-detail", kwargs={"pk": user.pubkey})
        invalid_data = {"handle": "__dsi-="}

        response = client.put(url, invalid_data, format="json")
        
        assert response.status_code == 400
        assert response.data.get("message") == "Failed to update station"
        assert response.data.get("data") is not None

    def test_has_station(self, client, user, station):
        """Test if a user has a station."""
        client.force_authenticate(user=user)
        url = reverse("station-has-station")

        response = client.get(url)

        assert response.status_code == 200
        assert response.data.get("message") is None
        assert response.data.get("data") == True

    def test_retrieve_with_albums_and_relations(self, client, user, station, station_picture, album, album_cover, track, default_genre, default_mood, test_img_file):
        """Test retrieving a station with albums and relations."""
        client.force_authenticate(user=user)
        url = reverse("station-retrieve-with-albums-and-relations", kwargs={"pk": user.pubkey})

        response = client.get(url)

        assert response.status_code == 200
        assert response.data.get("message") is None
        assert response.data.get("data") is not None

    def test_retrieve_with_albums_and_relations_error(self, client, user, station, station_picture, album, album_cover, track, default_genre, default_mood, test_img_file):
        """Test retrieving a station with albums and relations."""
        client.force_authenticate(user=user)
        url = reverse("station-retrieve-with-albums-and-relations", kwargs={"pk": "wrong_pubkey"})

        response = client.get(url)

        assert response.status_code == 404
        assert response.data.get("message") == "No station found"
        assert response.data.get("data") is not None

