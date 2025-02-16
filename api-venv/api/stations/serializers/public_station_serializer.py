from rest_framework import serializers
from ..models import Station
from albums.serializers import StationAlbumSerializer

class PublicStationSerializer(serializers.ModelSerializer):
    albums = StationAlbumSerializer(many=True)
    class Meta:
        model = Station
        fields = [
            'albums',
            'created',
            'description',
            'email',
            'handle',
            'name',
            'picture'
        ]


