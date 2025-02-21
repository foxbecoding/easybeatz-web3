from rest_framework import serializers
from ..models import Station
from albums.models import Album

class AlbumsField(serializers.RelatedField):
    def to_representation(self, value: Album):
        return {
            "aid": value.aid,
            "bio": value.bio,
            "cover": value.cover.cover_url,
            "title": value.title,
            "tracks_count": value.tracks_count,
        }

class StationWithAlbumsAndRelationsSerializer(serializers.ModelSerializer):
    albums = AlbumsField(many=True, read_only=True)
    is_owner = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()
    formatted_launched_date = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = [
            'albums',
            'description',
            'email',
            'formatted_launched_date',
            'handle',
            'is_owner',
            'name',
            'picture',
        ]

    def get_is_owner(self, obj):
        return self.context['is_owner']

    def get_formatted_launched_date(self, obj: Station):
        return obj.formatted_launched_date

    def get_picture(self, obj):
        return str(obj.picture_url)
