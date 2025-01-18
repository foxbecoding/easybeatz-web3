
from rest_framework import serializers
from ..models import Station

class EditStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = [
            'name', 
            'handle', 
            'description', 
            'email',
        ]

