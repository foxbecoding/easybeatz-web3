from rest_framework import serializers
from ..models import Station
from users.models import User

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = [
            'user',
            'name', 
            'handle', 
            'description', 
            'email',
        ]

        extra_kwargs = {"user": {"read_only": True}}

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

