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
        request = self.context['request']
        user = User.objects.filter(pubkey=request.user).first()
        station = Station(user.pk, **validated_data).save()
        return station
