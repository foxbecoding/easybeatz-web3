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
        handle = attrs.get('handle')

        if handle and not str(handle).isalnum():
            raise serializers.ValidationError({"handle": "Handle can only contain strings and numbers."})
        return attrs

    def create(self, validated_data):
        """ Ensure 'user' is included when creating a station """
        if 'user' not in validated_data:
            raise serializers.ValidationError({"user": "This field is required."})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """ Exclude 'user' from the update process """
        validated_data.pop('user', None)  # Remove user field if present
        return super().update(instance, validated_data)
