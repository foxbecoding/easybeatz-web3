from rest_framework import serializers
from ..models import Station

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = [
            'name', 
            'handle', 
            'description', 
            'email',
        ]

    def validate(self, attrs):

        # check if handle is valid
        if attrs['handle'] and not str(attrs['handle']).isalnum():
            raise serializers.ValidationError({"handle": "Handle can only contain strings and numbers."})
        return attrs
