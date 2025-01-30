from rest_framework import serializers
from ..models import TrackMp3

class CreateTrackMp3Serializer(serializers.ModelSerializer):
    class Meta:
        model = TrackMp3
        fields = [
            'track',
            'audio',
        ]
