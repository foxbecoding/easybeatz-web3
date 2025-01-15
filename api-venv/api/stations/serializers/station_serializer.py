from rest_framework import serializers
from ..models import Station

class StationSerializer(serializers.ModelSerializer):
    is_owner = serializers.BooleanField(read_only=True) 
    
    class Meta:
        model = Station
        fields = [
            'name', 
            'handle', 
            'description', 
            'email',
            'is_owner',
            'created'
        ]
