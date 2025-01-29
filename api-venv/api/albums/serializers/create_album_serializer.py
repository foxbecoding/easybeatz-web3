from rest_framework import serializers
from ..models import Album

class CreateAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = [
            'station',
            'title',
            'bio',
        ]
