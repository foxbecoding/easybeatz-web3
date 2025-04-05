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

