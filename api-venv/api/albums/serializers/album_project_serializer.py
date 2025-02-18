from rest_framework import serializers
from stations.models import Station, StationPicture
from ..models import Album, AlbumCover, Track, TrackDisplay, TrackPrice, TrackExclusivePrice
from moods.models import Mood
from genres.models import Genre
from datetime import datetime

class AlbumStationField(serializers.RelatedField):
    def to_representation(self, value):
        data = {
            "handle": value.handle,
            "picture": value.picture.url,
            "pubkey": value.user.pubkey
        }
        return data

