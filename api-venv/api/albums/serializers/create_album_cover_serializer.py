from rest_framework import serializers
from ..models import AlbumCover

class CreateAlbumCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumCover
        fields = [
            'album',
            'picture',
        ]
