from rest_framework import serializers
from ..models import Station
from albums.models import Album

class AlbumsField(serializers.RelatedField):
    def to_representation(self, value: Album):

        data = {
            "aid": value.aid,
            "bio": value.bio,
            "title": value.title,
            "tracks_count": value.tracks_count,
            "cover": value.cover.picture.url if value.cover else None,
        }
        return data

class StationWithAlbumsAndRelationsSerializer(serializers.ModelSerializer):
    albums = AlbumsField(many=True, read_only=True)
    is_owner = serializers.SerializerMethodField()
    picture = StationPictureField(read_only=True)
    formatted_launched_date = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = [
            'albums',
            'description',
            'email',
            'handle',
            'is_owner',
            'formatted_launched_date',
            'name',
            'picture',
        ]

    def get_is_owner(self, obj):
        return self.context['is_owner']

    def get_formatted_launched_date(self, obj: Station):
        return obj.formatted_launched_date
