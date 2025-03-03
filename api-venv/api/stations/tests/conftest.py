import pytest
from users.tests.conftest import default_user
from stations.models import Station, StationPicture
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

@pytest.fixture
def default_station(db, default_user):
    """Create a test station linked to the test user"""
    return Station.objects.create(
        user=default_user,
        name="Test Station",
        handle="teststation",
        description="This is a test station.",
        email="station@example.com",
    )

