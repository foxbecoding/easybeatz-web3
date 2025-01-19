from rest_framework import serializers
from ..models import Station

class PublicStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = [
            'name', 
            'handle', 
            'description', 
            'email',
            'created'
        ]
