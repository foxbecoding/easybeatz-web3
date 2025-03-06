from rest_framework import serializers
from ..models import StationPicture
from PIL import Image

class StationPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationPicture
        fields = ['picture']

    def validate_picture(self, value):
        # Ensure the file is not empty
        if not value:
            raise serializers.ValidationError("This field cannot be empty.")

        # Allowed file types
        allowed_formats = ['png', 'jpeg', 'jpg', 'avif', 'webp', 'bmp']

        # Check file size
        # max_size_mb = 6
        # if value.size > max_size_mb * 1024 * 1024:
        #     raise serializers.ValidationError(f"Image file size must not exceed {max_size_mb}MB.")

        # Check image format
        try:
            image = Image.open(value)
            if str(image.format).lower() not in allowed_formats:
                raise serializers.ValidationError(f"Unsupported image format. Allowed formats are: {', '.join(allowed_formats)}.")

            # Check image dimensions
            # width, height = image.size
            # if width < 98 or height < 98:
            #     raise serializers.ValidationError("Image dimensions must be at least 98x98 pixels.")
            #
            # # Ensure it's a square
            # if width != height:
            #     raise serializers.ValidationError("Image must be a square(1:1 ration)")

        except Exception as e:
            raise serializers.ValidationError("Invalid image file.") 

        return value

    def create(self, validated_data):
        """Ensure 'station' is assigned manually (not expected in validated_data)."""
        station = self.context["station"] # Get station from request context

        validated_data["station"] = station 
        return super().create(validated_data)

