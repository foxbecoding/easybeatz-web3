from rest_framework import serializers
from albums.models import Track

class AlbumField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "aid": value.aid,
            "title": value.title,
            "cover": value.cover.cover_url
        }

class DisplayField(serializers.RelatedField):
    def to_representation(self, value):
        return value.display_url

class MoodField(serializers.RelatedField):
    def to_representation(self, value):
        return { "name": value.name, "slug": value.slug }

class PriceField(serializers.RelatedField):
    def to_representation(self, value):
        return value.value

class ExclusivePriceField(serializers.RelatedField):
    def to_representation(self, value):
        return value.value

class TrackPageSerializer(serializers.ModelSerializer):
    album = AlbumField(read_only=True)
    display = DisplayField(read_only=True)
    price = PriceField(read_only=True)
    mood = MoodField(read_only=True)
    exclusive_price = ExclusivePriceField(read_only=True)
    genres = serializers.SerializerMethodField()
    stems = serializers.SerializerMethodField()
    station = serializers.SerializerMethodField()
    formatted_duration = serializers.SerializerMethodField()
    total_favorite_count = serializers.SerializerMethodField()
    has_wav_file = serializers.SerializerMethodField()
    uploaded_at = serializers.SerializerMethodField()

    def get_station(self, obj):
        station = obj.album.station 

        return {
            "name": station.name,
            "handle": station.handle,
            "pubkey": station.user.pubkey,
            "picture": station.picture.picture_url
        }

    def get_uploaded_at(self, obj):
        return obj.uploaded_at

    def get_formatted_duration(self, obj):
        return obj.formatted_duration

    def get_has_wav_file(self, obj):
        return obj.has_wav_file

    def get_stems(self, obj):
        stems = [stem.name for stem in obj.stems.all()]
        return stems
    
    def get_genres(self, obj):
        genres = [{ "name": genre.name, "slug": genre.slug } for genre in obj.genres.all()]
        return genres[0]

    def get_total_favorite_count(self, obj):
        return obj.track_favorite_set.all().count()

    class Meta:
        model = Track
        fields = [
            "bpm",
            "display",
            "duration",
            "exclusive_price",
            "formatted_duration",
            "total_favorite_count",
            "has_wav_file",
            "uploaded_at",
            "genres",
            "stems",
            "mood",
            "order_no",
            "price",
            "tid",
            "title",
            "album",
            "station",
        ]
