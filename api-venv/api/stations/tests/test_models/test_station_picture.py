import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from stations.models import Station, StationPicture

@pytest.mark.django_db
def test_station_picture_creation(default_station):
    """Test that a StationPicture instance is correctly created."""
    image_content = b"fake image data"
    image = SimpleUploadedFile("test_image.jpg", image_content, content_type="image/jpeg")
    
    station_picture = StationPicture.objects.create(station=default_station, picture=image)

    assert station_picture is not None
    assert station_picture.station == default_station
    assert station_picture.picture.name.startswith("station/pictures/")
    assert station_picture.picture_url is not None


@pytest.mark.django_db
def test_custom_image_upload_path(default_station_picture):
    """Test that the image is uploaded to the correct directory."""
    assert default_station_picture.picture.name.startswith("station/pictures/")
    assert default_station_picture.picture.name.endswith(".jpg")

@pytest.mark.django_db
def test_picture_url_property(default_station_picture):
    """Test that the picture_url property returns a valid URL."""
    assert default_station_picture.picture_url is not None
    assert default_station_picture.picture_url.endswith(".jpg")


