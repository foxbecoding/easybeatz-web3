from rest_framework import serializers
from ..models import Station, StationPicture
from albums.models import Album
from datetime import datetime

class StationPictureField(serializers.RelatedField):
    def to_representation(self, value: StationPicture):
        return str(value.picture.url)

class AlbumsField(serializers.RelatedField):
    def to_representation(self, value: Album):
        data = {
            "aid": value.aid,
            "bio": value.bio,
            "title": value.title,
            "tracks_count": getattr(value, "tracks_count", 0),
            "cover": value.cover.picture.url if value.cover else None,
        }
        return data

class PublicStationSerializer(serializers.ModelSerializer):
    albums = AlbumsField(many=True, read_only=True)
    is_owner = serializers.SerializerMethodField()
    launch_date = serializers.SerializerMethodField()
    picture = StationPictureField(read_only=True)

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
            'picture',
        ]

    def get_is_owner(self, obj):
        return self.context['is_owner']

    def get_launch_date(self, obj: Station):
        created_date = datetime.fromisoformat(str(obj.created).replace("Z", "+00:00"))
        return created_date.year
