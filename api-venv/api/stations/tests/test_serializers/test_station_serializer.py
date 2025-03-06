import pytest
from stations.serializers import StationSerializer
from users.tests.conftest import default_user
import logging

logger = logging.getLogger("stations")

@pytest.mark.django_db
class TestStationSerializer:
    @pytest.fixture
    def user(self, default_user):
        return default_user

    @pytest.fixture
    def station(self, default_station):
        return default_station

    def test_valid_station_serialization(self, station):
        """Test that a station serializes correctly with valid data."""
        serializer = StationSerializer(station)
        assert serializer.data["name"] == "Test Station"
        assert serializer.data["handle"] == "teststation"
        assert serializer.data["description"] == "This is a test station."
        assert serializer.data["email"] == "station@example.com"

    def test_invalid_handle_validation(self, user):
        """Test that validation fails when handle contains special characters."""
        invalid_data = {
            "user": user.id,
            "name": "Invalid Station",
            "handle": "invalid_handle!",  # Invalid handle (special character)
            "description": "Invalid handle test",
            "email": "test2@example.com",
        }

        serializer = StationSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert "handle" in serializer.errors
