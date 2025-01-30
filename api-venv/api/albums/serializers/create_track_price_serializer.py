from rest_framework import serializers
from ..models import TrackPrice

class CreateTrackPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackPrice
        fields = [
            'track',
            'value',
        ]
