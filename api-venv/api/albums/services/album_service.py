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
        return {
            'title': self.form_data.get(f'tracks[{index}][title]'),
            'genres': [self.form_data.get(f'tracks[{index}][genres][{gi}]') for gi in range(genre_count)],
            'mood': self.form_data.get(f'tracks[{index}][mood]'),
            'mp3': self.form_data.get(f'tracks[{index}][mp3]'),
            'wav': self.form_data.get(f'tracks[{index}][wav]'),
            'bpm': self.form_data.get(f'tracks[{index}][bpm]'),
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

    def is_valid(self):
        if not self._is_album_data_valid():
            return False
        if not self._is_tracks_data_valid():
            return False
        return True

    def _is_album_data_valid(self):
        serializer = AlbumFormSerializer(data=self.album_data)
        if not serializer.is_valid():
            self.errors.append(serializer.errors)
            return False
        return True 

    def _is_tracks_data_valid(self):
        for index, track_data in enumerate(self.tracks_data):
            serializer = TrackFormSerializer(data=track_data, context={'track_data': track_data, 'index': index})
            if not serializer.is_valid():
                self.errors.append(serializer.errors)
                return False
        return True

class AlbumCreator:
    def __init__(self, album_data, tracks_data, user):
        self.album_data = album_data
        self.tracks_data = tracks_data
        self.user = user

    def _save_model_data(self, data, model):
        instance = model(**data)
        instance.save()
        return instance

    @transaction.atomic
    def create_album(self):
        station = get_object_or_404(Station, pk=self.user.pk)
        album = self._save_model_data({ "station": station, "title": self.album_data['title'], "bio": self.album_data['bio'] }, Album)
        self._save_model_data({ "album": album, "picture": self.album_data['cover'] }, AlbumCover)

        for index, track_data in enumerate(self.tracks_data):
            # 1.) Save Track
            genres = Genre.objects.filter(pk__in=track_data['genres'])
            mood = get_object_or_404(Mood, pk=track_data['mood'])
            track_model_data = {
                'album': album,
                'title': track_data['title'],
                'bpm': track_data['bpm'],
                'mood': mood,
                'order_no': index
            }
            track = self._save_model_data(track_model_data, Track)
            track.genres.set(genres)

            # 2.) Save TrackPrice
            self._save_model_data({ 'track': track, 'value': track_data['price'] }, TrackPrice)

            # 3.) Save TrackMp3
            self._save_model_data({ 'track': track, 'audio': track_data['mp3'] }, TrackMp3)

            # 4.) Save TrackWav
            if track_data['wav']:
                self._save_model_data({ 'track': track, 'audio': track_data['wav'] }, TrackWav)

            # 5.) Save TrackExclusivePrice
                self._save_model_data({ 'track': track, 'value': track_data['exclusive_price'] }, TrackExclusivePrice)

            # 6.) Bulk create collaborators
            collaborators = [TrackCollaborator(track=track, pubkey=collab) for collab in track_data['collaborators']]
            TrackCollaborator.objects.bulk_create(collaborators)

            # 7.) Bulk create stems
            stems = [TrackStem(track=track, name=stem['name'], audio=stem['file']) for stem in track_data['stems']]
            TrackStem.objects.bulk_create(stems)

        return album
