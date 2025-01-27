from types import TracebackType
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from users.models import User
from stations.models import Station
from pprint import pprint

class AlbumProjectService:
    def __init__(self, data) -> None:
        self.form_data = data
        self.album_form_data = {}
        self.tracks_form_data = []
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
            genre_count = int(self.form_data.get(f'tracks[{i}][genre_count]'))
            collab_count = int(self.form_data.get(f'tracks[{i}][collab_count]'))
            stem_count = int(self.form_data.get(f'tracks[{i}][stem_count]'))
            track = {
                'index': i,
                'title': self.form_data.get(f'tracks[{i}][title]'),
                'genres': [self.form_data.get(f'tracks[{i}][genres][{gi}]') for gi in range(genre_count)],
                'mood': self.form_data.get(f'tracks[{i}][mood]'),
                'mp3': self.form_data.get(f'tracks[{i}][mp3]'),
                'bpm': self.form_data.get(f'tracks[{i}][bpm]'),
                'has_exclusive': bool(self.form_data.get(f'tracks[{i}][has_exclusive]')),
                'price':self.form_data.get(f'tracks[{i}][price]'),
                'exclusive_price': self.form_data.get(f'tracks[{i}][exclusive_price]'),
                'collaborators': [self.form_data.get(f'tracks[{i}][collaborators][{ci}]') for ci in range(collab_count)],
                'stems': [self.__stem_form_data_builder(i, si) for si in range(stem_count)],
            }
            self.tracks_form_data.append(track)

    def __stem_form_data_builder(self, track_index, stem_index):
        return { 
            "name": self.form_data.get(f'tracks[{track_index}][stems][{stem_index}][name]'),
            "file": self.form_data.get(f'tracks[{track_index}][stems][{stem_index}][file]')
        }

    def __validate_album_form_data(self):
        pass

    def is_form_data_valid(self) -> bool:
        return False 

