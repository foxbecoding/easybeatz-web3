from rest_framework import serializers
from ..models import TrackWav

class CreateTrackWavSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackWav
        fields = [
            'track',
            'audio',
        ]
