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
        request = self.context['request']
        
        # check if handle is valid
        if attrs['handle'] and not str(attrs['handle']).isalnum():
            raise serializers.ValidationError({"handle": "Handle can only contain strings and numbers."})


        user = User.objects.filter(pubkey=request.user).first()

        station_ins = Station(
            user=user,
            name=attrs['name'],
            handle=attrs['handle'],
            description=attrs['description'],
            email=attrs['email'],
        )

        station_ins.save()

        return attrs
