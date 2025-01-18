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
        return station_ins.save()

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.handle = validated_data.get('handle', instance.handle)
        instance.description = validated_data.get('description', instance.description)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
