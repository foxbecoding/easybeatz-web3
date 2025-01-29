from rest_framework import serializers
from ..models import TrackStem

class CreateTrackStemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackStem
        fields = [
            'track',
            'name',
            'audio',
        ]
