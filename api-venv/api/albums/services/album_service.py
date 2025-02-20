from django.db import transaction
from django.shortcuts import get_object_or_404
from ..models import *
from genres.models import Genre
from moods.models import Mood
from stations.models import Station
from ..serializers import AlbumFormSerializer, TrackFormSerializer

class FormDataProcessor:
    def __init__(self, request_data) -> None:
        self.form_data = request_data
        self.album_form_data = {}
        self.tracks_form_data = []

    def set_form_data(self):
        self._set_album_form_data()
        self._set_tracks_form_data()

    def _set_album_form_data(self):
        self.album_form_data = {
            "title": self.form_data.get('album[title]'),
            "bio": self.form_data.get('album[bio]'),
            "cover": self.form_data.get('album[cover]')
        }

    def _set_tracks_form_data(self):
        track_count = int(self.form_data.get('track_count', 0))
        for i in range(track_count):
            track = self._track_form_data_builder(i) 
            self.tracks_form_data.append(track)

    def _track_form_data_builder(self, index):
        genre_count = int(self.form_data.get(f'tracks[{index}][genre_count]', 0))
        collab_count = int(self.form_data.get(f'tracks[{index}][collab_count]', 0))
        stem_count = int(self.form_data.get(f'tracks[{index}][stem_count]', 0))
        has_exclusive = self.form_data.get(f'tracks[{index}][has_exclusive]') == 'True'
        return {
            'title': self.form_data.get(f'tracks[{index}][title]'),
            'genres': [self.form_data.get(f'tracks[{index}][genres][{gi}]') for gi in range(genre_count)],
            'mood': self.form_data.get(f'tracks[{index}][mood]'),
            'mp3': self.form_data.get(f'tracks[{index}][mp3]'),
            'wav': self.form_data.get(f'tracks[{index}][wav]'),
            'bpm': self.form_data.get(f'tracks[{index}][bpm]'),
            'has_exclusive': has_exclusive,
            'price': self.form_data.get(f'tracks[{index}][price]'),
            'exclusive_price': self.form_data.get(f'tracks[{index}][exclusive_price]'),
            'collaborators': [self.form_data.get(f'tracks[{index}][collaborators][{ci}]') for ci in range(collab_count)],
            'stems': [self._stem_form_data_builder(index, si) for si in range(stem_count)],
        }

    def _stem_form_data_builder(self, track_index, stem_index):
        return { 
            "name": self.form_data.get(f'tracks[{track_index}][stems][{stem_index}][name]'),
            "file": self.form_data.get(f'tracks[{track_index}][stems][{stem_index}][file]')
        }

class AlbumValidator:
    def __init__(self, album_data, tracks_data):
        self.album_data = album_data
        self.tracks_data = tracks_data
        self.errors = []

