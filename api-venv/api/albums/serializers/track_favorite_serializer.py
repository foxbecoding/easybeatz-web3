from rest_framework import serializers
from albums.models import TrackFavorite

class TrackFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackFavorite
        fields = [
            'track',
            'user',
        ]
