from rest_framework.schemas.coreapi import serializers
from ..models import *
from genres.models import Genre
from moods.models import Mood
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
        for index, track_data in enumerate(self.tracks_form_data):
            serializer = TrackFormSerializer(data=track_data, context={'track_data': track_data, 'index': index})
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

    def __track_model_data_builder(self, album: Album):
        tracks_data = []
        for index, track in enumerate(self.tracks_form_data):
            genres =  Genre.objects.filter(pk__in=track['genres'])
            mood = Mood.objects.get(pk=track['mood'])
            data = {
                'album': album,
                'title': track['title'],
                'genres': genres,
                'mood': mood,
                'bpm': track['bpm'],
                'order_no': index
            }
            tracks_data.append(data)

    def __save_model_data(self, data, model):
        instance = model(**data)
        instance.save()
        return instance

    def save(self, station: Station):
        # Save Album data
        album = self.__save_model_data({ "station": station, "title": self.album_form_data['title'], "bio": self.album_form_data['bio'] }, Album)

        # Save AlbumCover
        self.__save_model_data({ "album": album, "picture": self.album_form_data['cover'] }, AlbumCover)

        # Process for save Tracks and related models
        for index, track_data in enumerate(self.tracks_form_data):

            # 1.) Save Track
            genres =  Genre.objects.filter(pk__in=track_data['genres'])
            mood = Mood.objects.get(pk=track_data['mood'])
            track_model_data = {
                'album': album,
                'title': track_data['title'],
                'bpm': track_data['bpm'],
                'mood': mood,
                'order_no': index
            }
            track = self.__save_model_data(track_model_data, Track)
            track.genres.set(genres)

            # 2.) Save TrackPrice
            self.__save_model_data({ 'track': track, 'value': track_data['price'] }, TrackPrice)

            # 3.) Save TrackMp3
            self.__save_model_data({ 'track': track, 'audio': track_data['mp3'] }, TrackMp3)

            # 4.) Save TrackWav
            if track_data['wav']:
                self.__save_model_data({ 'track': track, 'audio': track_data['wav'] }, TrackWav)

            # 5.) Save TrackCollaborators
            if track_data['collaborators']:
                collabs = []
                for collab in track_data['collaborators']:
                    collab_data = TrackCollaborator(track=track, pubkey=collab)
                    collabs.append(collab_data)
                TrackCollaborator.objects.bulk_create(collabs)

            if track_data['has_exclusive']:
                # 6.) Save TrackExclusivePrice
                self.__save_model_data({ 'track': track, 'value': track_data['exclusive_price'] }, TrackExclusivePrice)

                # 7.) Save TrackStems
                stems = []
                for stem in track_data['stems']:
                    stem_data = TrackStem(track=track, name=stem['name'], audio=stem['file'])
                    stems.append(stem_data)
                TrackStem.objects.bulk_create(stems)
