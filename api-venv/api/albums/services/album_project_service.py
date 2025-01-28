from rest_framework.schemas.coreapi import serializers
from users.models import User
from stations.models import Station
from ..serializers import AlbumFormSerializer, TrackFormSerializer

class AlbumProjectService:
    def __init__(self, request_data) -> None:
        self.form_data = request_data
        self.album_form_data = {}
        self.tracks_form_data = []
        self.errors = None
        self.__set_form_data()

    def __set_form_data(self):
        self.__set_album_form_data()
        self.__set_tracks_form_data()

    def __set_album_form_data(self):
        self.album_form_data = {
            "title": self.form_data.get(f'album[title]'),
            "bio": self.form_data.get(f'album[bio]'),
            "cover": self.form_data.get(f'album[cover]')
        }

    def __set_tracks_form_data(self):
        track_count = int(self.form_data.get(f'track_count'))
        for i in range(track_count):
            track = self.__track_form_data_builder(i) 
            self.tracks_form_data.append(track)

    def __track_form_data_builder(self, index):
        genre_count = int(self.form_data.get(f'tracks[{index}][genre_count]'))
        collab_count = int(self.form_data.get(f'tracks[{index}][collab_count]'))
        stem_count = int(self.form_data.get(f'tracks[{index}][stem_count]'))
        has_exclusive = self.form_data.get(f'tracks[{index}][has_exclusive]') == 'True'
        return {
            'index': index,
            'title': self.form_data.get(f'tracks[{index}][title]'),
            'genres': [self.form_data.get(f'tracks[{index}][genres][{gi}]') for gi in range(genre_count)],
            'mood': self.form_data.get(f'tracks[{index}][mood]'),
            'mp3': self.form_data.get(f'tracks[{index}][mp3]'),
            'wav': self.form_data.get(f'tracks[{index}][wav]'),
            'bpm': self.form_data.get(f'tracks[{index}][bpm]'),
            'has_exclusive': has_exclusive,
            'price':self.form_data.get(f'tracks[{index}][price]'),
            'exclusive_price': self.form_data.get(f'tracks[{index}][exclusive_price]'),
            'collaborators': [self.form_data.get(f'tracks[{index}][collaborators][{ci}]') for ci in range(collab_count)],
            'stems': [self.__stem_form_data_builder(index, si) for si in range(stem_count)],
        }

    def __stem_form_data_builder(self, track_index, stem_index):
        return { 
            "name": self.form_data.get(f'tracks[{track_index}][stems][{stem_index}][name]'),
            "file": self.form_data.get(f'tracks[{track_index}][stems][{stem_index}][file]')
        }

    def __is_album_form_data_valid(self) -> bool:
        album_serializer = AlbumFormSerializer(data=self.album_form_data)
        if not album_serializer.is_valid():
            self.errors = album_serializer.errors
            return False
        return True 

    def __is_tracks_form_data_valid(self) -> bool:
        serializer = TrackFormSerializer(data=self.tracks_form_data, context={'tracks_form_data': self.tracks_form_data}, many=True)
        if not serializer.is_valid():
            self.errors = serializer.errors
            return False
        return True

    def is_form_data_valid(self) -> bool:
        if not self.__is_album_form_data_valid():
            return False
        if not self.__is_tracks_form_data_valid():
            return False
        self.errors = None
        return True

