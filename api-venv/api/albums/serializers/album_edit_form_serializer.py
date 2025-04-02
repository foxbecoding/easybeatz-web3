from rest_framework import serializers
from albums.models import Album

class AlbumEditFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = [
            'title',
            'bio',
        ]
