from rest_framework import serializers
from ..models import Album, TrackPrice
from moods.models import Mood

class AlbumStationField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "handle": value.handle,
            "name": value.name,
            "picture": value.picture_url,
            "pubkey": value.user.pubkey
        }

class AlbumGenreField(serializers.RelatedField):
    def to_representation(self, value):
        return { "name": value.name, "slug": value.slug }

class AlbumCoverField(serializers.RelatedField):
    def to_representation(self, value):
        return value.picture.url

class AlbumTracksField(serializers.RelatedField):
    def to_representation(self, value):
        price: TrackPrice = value.price
        exclusive_price = getattr(value, "exclusive_price", None)
        mood: Mood = value.mood
        genres = [{"name": genre.name, "slug": genre.slug} for genre in value.genres.all()]

        return {
            "bpm": value.bpm,
            "display": value.display_url,
            "duration": value.duration,
            "exclusive_price": exclusive_price.value if exclusive_price else None,
            "formatted_duration": value.formatted_duration,
            "genres": genres[0],
            "mood": { "name": mood.name, "slug": mood.slug },
            "order_no": value.order_no,
            "price": price.value,
            "tid": value.tid,
            "title": value.title,
        }

class AlbumWithTracksSerializer(serializers.ModelSerializer):
    station = AlbumStationField(read_only=True)
    tracks = AlbumTracksField(many=True, read_only=True)
    total_duration = serializers.IntegerField()
    cover = AlbumCoverField(read_only=True)
    uploaded_at = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    def get_uploaded_at(self, obj):
        return obj.uploaded_at

    class Meta:
        model = Album
        fields = [
            'aid',
            'bio',
            'cover',
            'station',
            'title',
            'total_duration',
            'tracks',
            'uploaded_at',
            'is_owner'
        ]

    def get_is_owner(self, obj):
        return self.context['is_owner']

