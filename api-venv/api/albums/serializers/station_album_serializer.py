from rest_framework import serializers
from ..models import Album, AlbumCover

class StationAlbumSerializer(serializers.ModelSerializer):
    cover_picture = serializers.SerializerMethodField()
    tracks_count = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = [
            'aid',
            'bio',
            'title',
            'tracks_count',
            'cover_picture'
        ]

    def get_tracks_count(self, obj):
        return obj.tracks.count()

    def get_cover_picture(self, obj):
        cover: AlbumCover = obj.cover
        return str(cover.picture)
