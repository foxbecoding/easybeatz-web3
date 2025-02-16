from rest_framework import serializers
from ..models import Album, AlbumCover

class AlbumCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumCover
        fields = ['picture']

class StationAlbumSerializer(serializers.ModelSerializer):
    cover = AlbumCoverSerializer()
    tracks_count = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = [
            'aid',
            'bio',
            'title',
            'tracks_count',
            'cover'
        ]

    def get_tracks_count(self, obj):
        return obj.tracks.count()
