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

@pytest.fixture
def default_station_picture(db, default_station):
    """Create a test StationPicture with an in-memory image"""
    # Create an in-memory image
    image = Image.new("RGB", (100, 100), color="red")
    image_io = io.BytesIO()
    image.save(image_io, format="JPEG")
    image_io.seek(0)

    uploaded_image = SimpleUploadedFile(
        "test_image.jpg",
        image_io.getvalue(),
        content_type="image/jpeg"
    )

    return StationPicture.objects.create(
        station=default_station,
        picture=uploaded_image,
    )
