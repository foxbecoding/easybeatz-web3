from rest_framework import serializers
from ..models import Station

class PublicStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = [
            'albums',
            'created',
            'description',
            'email',
            'handle',
            'name',
            'picture'
        ]
