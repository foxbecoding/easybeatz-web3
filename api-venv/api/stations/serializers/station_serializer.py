from rest_framework import serializers
from ..models import Station
from users.models import User

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
        handle = attrs['handle']

        # check if handle is valid
        if handle and not str(handle).isalnum():
            raise serializers.ValidationError({"handle": "Handle can only contain strings and numbers."})
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        user_ins = User.objects.filter(pubkey=request.user).first()

        station_ins = Station(
            user=user_ins,
            **validated_data
        )
        station_ins.save()
        return
