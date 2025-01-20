from rest_framework import serializers
from ..models import StationPicture
from PIL import Image

class StationPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationPicture
        fields = ['station', 'picture']

    def validate_picture(self, value):
        # Allowed file types
        allowed_formats = ['png', 'jpeg', 'jpg', 'avif']

        # Check file size
        max_size_mb = 6
        if value.size > max_size_mb * 1024 * 1024:
            raise serializers.ValidationError({"picture": f"Image file size must not exceed {max_size_mb}MB."})

        # Check image format
        try:
            image = Image.open(value)
            if image.format.lower() not in allowed_formats:
                raise serializers.ValidationError({"picture": f"Unsupported image format. Allowed formats are: {', '.join(allowed_formats)}."})

            # Check image dimensions
            width, height = image.size
            if width < 98 or height < 98:
                raise serializers.ValidationError({"picture": "Image dimensions must be at least 98x98 pixels."})

            # Ensure it's a square
            if width != height:
                raise serializers.ValidationError("Image must be a square (equal width and height).")

        except Exception as e:
            raise serializers.ValidationError({"picture": "Invalid image file."}) 

        return value
