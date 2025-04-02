import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from albums.models import Album, Track
from genres.tests.conftest import default_genre
from moods.tests.conftest import default_mood
from stations.tests.conftest import default_station, default_station_picture
from users.tests.conftest import default_user
from users.tests.factories import UserFactory
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

    @pytest.fixture
    def mood(self, db, default_mood):
        """Fixture to create mood"""
        return default_mood

    @pytest.fixture
    def album(self, db, default_album):
        return default_album

    @pytest.fixture
    def album_with_tracks_and_relations(self, db, default_album_with_tracks_and_relations):
        """Fixture to create test album with tracks and relations"""
        return default_album_with_tracks_and_relations

    @pytest.fixture
    def request_data(self, db, genre, mood, test_mp3_file, test_wav_file, test_wav_file2, test_img_file):
        """Fixture for test request data"""
        return {
            "album[title]": "Test album title",
            "album[cover]": test_img_file,
            "album[bio]": "Test album bio",
            "track_count": 1,
            "tracks[0][genre_count]": 1,
            "tracks[0][collab_count]": 1,
            "tracks[0][stem_count]": 1,
            "tracks[0][bpm]": 120,
            "tracks[0][collaborators][0]": ["some_pubkey"],
            "tracks[0][exclusive_price]": 369,
            "tracks[0][genres][0]": [str(genre.pk)],
            "tracks[0][mood]": str(mood.pk),
            "tracks[0][mp3]": test_mp3_file,
            "tracks[0][price]": 36,
            "tracks[0][title]": "Test track",
            "tracks[0][wav]": test_wav_file,
            "tracks[0][stems][0][name]": "snare",
            "tracks[0][stems][0][file]": test_wav_file2,
        } 

    @pytest.fixture
    def invalid_request_data(self, db):
        """Fixture for test invalid_request_data"""
        return {
            "wrong_data": 'invalid'
        }

    @pytest.fixture
    def track_request_data(self, db, genre, mood, test_mp3_file, test_wav_file, test_wav_file2, test_img_file):
        """Fixture for test request data"""
        return {
            "track[genre_count]": 1,
            "track[collab_count]": 1,
            "track[stem_count]": 1,
            "track[bpm]": 120,
            "track[collaborators][0]": ["some_pubkey"],
            "track[exclusive_price]": 369,
            "track[genres][0]": [str(genre.pk)],
            "track[mood]": str(mood.pk),
            "track[mp3]": test_mp3_file,
            "track[price]": 36,
            "track[title]": "Test track",
            "track[wav]": test_wav_file,
            "track[stems][0][name]": "snare",
            "track[stems][0][file]": test_wav_file2,
        }
    
    @pytest.fixture
    def invalid_track_request_data(self, db, genre, mood, test_mp3_file, test_wav_file, test_wav_file2, test_img_file):
        """Fixture for test request data"""
        return {
            "track[genre_count]": 1,
            "track[collab_count]": 1,
            "track[stem_count]": 1,
            "track[bpm]": 120,
            "track[collaborators][0]": ["some_pubkey"],
            "track[exclusive_price]": 369,
            "track[genres][0]": [str(genre.pk)],
            "track[mood]": str(mood.pk),
            "track[mp3]": "test_mp3_file.mp3",
            "track[price]": 36,
            "track[title]": "Test track",
            "track[wav]": test_wav_file,
            "track[stems][0][name]": "snare",
            "track[stems][0][file]": test_wav_file2,
        }

    @pytest.mark.django_db
    def test_album_update_view(self, db, client, user, station, album):
        client.force_authenticate(user=user)
        url = reverse("album-detail", kwargs={"pk": album.aid})
        updated_data = {"title": "New title", "bio": "New bio"}
        response = client.put(url, updated_data)

        assert response.status_code == status.HTTP_202_ACCEPTED
        album.refresh_from_db()
        assert album.title == "New title"
        assert album.bio == "New bio"

    @pytest.mark.django_db
    def test_album_update_view_error(self, db, client, user, station, album):
        client.force_authenticate(user=user)
        url = reverse("album-detail", kwargs={"pk": album.aid})
        updated_data = {"bio": "New bio"}
        response = client.put(url, updated_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("message") == "Failed to update album"
        assert response.data.get("data") is not None

    @pytest.mark.django_db 
    def test_non_album_owner_cannot_update(self, db, client, user, station, album):
        client.force_authenticate(user=user)
        url = reverse("album-detail", kwargs={"pk": "some id"})
        updated_data = {"title": "New title", "bio": "new bio"}
        response = client.put(url, updated_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_unauthenticated_cannot_update_album_view(self, db, client):
        url = reverse("album-detail", kwargs={"pk": None})
        response = client.put(url, None)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
   
    @pytest.mark.django_db
    def test_add_track_view(self, db, client, user, station, album, track_request_data):
        client.force_authenticate(user=user)
        url = reverse("album-add-track", kwargs={"pk":album.aid})
        response = client.post(url, track_request_data, format="multipart")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("message") == "Track added successfully"
        assert response.data.get("data") is None

        assert Album.albums.with_tracks_and_relations(album.aid) is not None
        track_qs = Track.objects.all()
        assert track_qs.count() > 0
    
    @pytest.mark.django_db
    def test_add_track_view_error(self, db, client, user, station, album, invalid_track_request_data):
        client.force_authenticate(user=user)
        url = reverse("album-add-track", kwargs={"pk":album.aid})
        response = client.post(url, invalid_track_request_data, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("message") == "Invalid track details"
        assert response.data.get("data")  is not None
    
    @pytest.mark.django_db
    def test_create_with_tracks_and_relations_view(self, db, client, user, station, request_data):
        client.force_authenticate(user=user)
        url = reverse("album-create-with-tracks-and-relations")
        response = client.post(url, request_data, format="multipart")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("message") == "Album created"
        assert response.data.get("data") is None

        album_qs = Album.objects.all()
        assert album_qs.count() > 0
        assert Album.albums.with_tracks_and_relations(album_qs.first().aid) is not None

        track_qs = Track.objects.all()
        assert track_qs.count() > 0

    @pytest.mark.django_db
    def test_unauthenticated_cannot_create_with_tracks_and_relations_view(self, db, client):
        url = reverse("album-create-with-tracks-and-relations")
        response = client.post(url, None, format="multipart")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_user_without_station_cannot_create_with_tracks_and_relations_view(self, db, client, user):
        client.force_authenticate(user=user)
        url = reverse("album-create-with-tracks-and-relations")
        response = client.post(url, None, format="multipart")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_create_with_tracks_and_relations_view_error(self, db, client, user, station, invalid_request_data):
        client.force_authenticate(user=user)
        url = reverse("album-create-with-tracks-and-relations")
        response = client.post(url, invalid_request_data, format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("message") == "Invalid album details"
        assert response.data.get("data")  is not None

    @pytest.mark.django_db
    def test_retrieve_with_tracks_and_relations_view(self, db, client, user, station, station_picture, album, album_with_tracks_and_relations):
        client.force_authenticate(user=user)
        url = reverse("album-retrieve-with-tracks-and-relations", kwargs={"pk": album.aid})
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("message") is None 
        assert response.data.get("data") is not None 

    @pytest.mark.django_db
    def test_retrieve_with_tracks_and_relations_view_error(self, db, client, user, station, station_picture, album, album_with_tracks_and_relations):
        client.force_authenticate(user=user)
        url = reverse("album-retrieve-with-tracks-and-relations", kwargs={"pk": "wrong_id"})
        response = client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("message") == "No album"
        assert response.data.get("data") is None

