from rest_framework import serializers
from ..models import Album, AlbumCover

class AlbumCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumCover
        fields = ['picture']

