import io
import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError
from stations.serializers import StationPictureSerializer

@pytest.mark.django_db
class TestStationPictureSerializer:

    def generate_test_image(self, format="JPEG"):
        """Helper function to create an in-memory image."""
        image = Image.new("RGB", (100, 100), color="red")
        image_io = io.BytesIO()
        image.save(image_io, format=format)
        image_io.seek(0)
        return SimpleUploadedFile(f"test_image.{format.lower()}", image_io.getvalue(), content_type=f"image/{format.lower()}")

    def test_valid_picture(self):
        """Test serializer accepts a valid image."""
        valid_image = self.generate_test_image("JPEG")
        serializer = StationPictureSerializer(data={"picture": valid_image})
        assert serializer.is_valid()

    def test_invalid_format(self):
        """Test serializer rejects an unsupported image format."""
        invalid_image = self.generate_test_image("TIFF")  # TIFF is not in the allowed formats
        serializer = StationPictureSerializer(data={"picture": invalid_image})

        assert not serializer.is_valid()

