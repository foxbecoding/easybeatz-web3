from rest_framework import serializers
from ..models import Track

class CreateTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = [
            'album',
            'genres',
            'moods',
            'title',
            'order_no'
        ]
