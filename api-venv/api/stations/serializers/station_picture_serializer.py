from rest_framework import serializers
from ..models import StationPicture

class StationPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationPicture
        fields = ['picture', 'image']
