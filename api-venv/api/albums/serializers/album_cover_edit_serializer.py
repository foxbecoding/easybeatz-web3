from rest_framework import serializers
from albums.models import AlbumCover
from PIL import Image

class AlbumCoverEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumCover
        fields = [ 'picture' ]


    def validate_picture(self, value):
        # Allowed file types
        allowed_formats = ['png', 'jpeg', 'jpg', 'avif', 'webp', 'bmp']

        try:
            image = Image.open(value)
            if str(image.format).lower() not in allowed_formats:
                raise serializers.ValidationError(f"Unsupported image format. Allowed formats are: {', '.join(allowed_formats)}.")

        except Exception as e:
            raise serializers.ValidationError("Invalid image file.") 

        return value
