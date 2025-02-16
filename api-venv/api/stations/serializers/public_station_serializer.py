from rest_framework import serializers
from ..models import Station
from albums.serializers import StationAlbumSerializer
from datetime import datetime

class PublicStationSerializer(serializers.ModelSerializer):
    albums = StationAlbumSerializer(many=True)
    is_owner = serializers.SerializerMethodField()
    launch_date = serializers.SerializerMethodField()
    station_picture = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = [
            'albums',
            'description',
            'email',
            'handle',
            'is_owner',
            'launch_date',
            'name',
            'station_picture',
        ]

    def get_is_owner(self, obj):
        return self.context['is_owner']

    def get_launch_date(self, obj: Station):
        created_date = datetime.fromisoformat(str(obj.created).replace("Z", "+00:00"))
        return created_date.year

    def get_station_picture(self, obj):
        picture = obj.picture.picture
        return str(picture)
