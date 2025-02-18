from rest_framework import serializers
from ..models import Album, TrackDisplay, TrackPrice
from moods.models import Mood

class AlbumStationField(serializers.RelatedField):
    def to_representation(self, value):
        data = {
            "handle": value.handle,
            "picture": value.picture_url,
            "pubkey": value.user.pubkey
        }
        return data

class AlbumCoverField(serializers.RelatedField):
    def to_representation(self, value):
        return value.picture.url

class TracksField(serializers.RelatedField):
    def to_representation(self, value):
        display: TrackDisplay = value.display
        price: TrackPrice = value.price
        exclusive_price: TrackExclusivePrice = value.exclusive_price
        mood: Mood = value.mood

        data = {
            "bpm": value.bpm,
            "duration": value.duration,
            "tid": value.tid,
            "title": value.title,
            "display": display.audio,
            "price": price.value,
            "exclusive_price": exclusive_price.value,
            "mood": { "name": mood.name, "slug": mood.slug }
        }
        return data

class AlbumProjectSerializer(serializers.ModelSerializer):
    station = AlbumStationField(read_only=True)
    tracks = TracksField(many=True, read_only=True)

    class Meta:
        model = Album
        fields = [
            'aid',
            'bio',
            'slug',
            'title',
            'total_duration',
            'station',
            'tracks',
        ]
