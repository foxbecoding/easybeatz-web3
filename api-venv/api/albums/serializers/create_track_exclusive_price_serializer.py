from rest_framework import serializers
from ..models import TrackExclusivePrice

class CreateTrackExclusivePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackExclusivePrice
        fields = [
            'track',
            'value',
        ]
