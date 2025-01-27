from rest_framework import serializers
from PIL import Image

class AlbumFormSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    bio = serializers.CharField(required=False)
    cover = serializers.ImageField()

    def validate_cover(self, value):
        # Allowed file types
        allowed_formats = ['png', 'jpeg', 'jpg', 'avif']

        try:
            image = Image.open(value)
            if str(image.format).lower() not in allowed_formats:
                raise serializers.ValidationError(f"Unsupported image format. Allowed formats are: {', '.join(allowed_formats)}.")

        except Exception as e:
            raise serializers.ValidationError("Invalid image file.") 

        return value

