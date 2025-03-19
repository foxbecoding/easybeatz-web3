from rest_framework import serializers
from albums.models import Track, TrackPrice, TrackExclusivePrice

class TrackEditFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = [
            'title',
            'genres',
            'mood',
            'bpm',
        ]

class TrackPriceEditFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackPrice
        fields = [
            'value',
        ]

