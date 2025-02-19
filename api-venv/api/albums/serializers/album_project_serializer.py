from rest_framework import serializers
from ..models import Album, TrackPrice
from moods.models import Mood

class AlbumStationField(serializers.RelatedField):
    def to_representation(self, value):
        data = {
            "handle": value.handle,
            "name": value.name,
            "picture": value.picture_url,
            "pubkey": value.user.pubkey
        }
        return data

class AlbumGenreField(serializers.RelatedField):
    def to_representation(self, value):
        return { "name": value.name, "slug": value.slug }

class AlbumCoverField(serializers.RelatedField):
    def to_representation(self, value):
        return value.picture.url

class AlbumTracksField(serializers.RelatedField):
    def to_representation(self, value):
        display: TrackDisplay = value.display
        price: TrackPrice = value.price
        exclusive_price = getattr(value, "exclusive_price", None)
        mood: Mood = value.mood
        genres = [{"name": genre.name, "slug": genre.slug} for genre in value.genres.all()]

        data = {
            "bpm": value.bpm,
            "duration": value.duration,
            "tid": value.tid,
            "title": value.title,
            "display": display.audio.url,
            "price": price.value,
            "exclusive_price": exclusive_price,
            "mood": { "name": mood.name, "slug": mood.slug },
            "genres": genres[0]
        }
        return data

class AlbumProjectSerializer(serializers.ModelSerializer):
    station = AlbumStationField(read_only=True)
    tracks = AlbumTracksField(many=True, read_only=True)
    total_duration = serializers.IntegerField()
    cover = AlbumCoverField(read_only=True)

    class Meta:
        model = Album
        fields = [
            'aid',
            'bio',
            'title',
            'total_duration',
            'cover',
            'station',
            'tracks',
        ]
