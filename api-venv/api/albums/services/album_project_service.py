from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from users.models import User
from stations.models import Station


class AlbumProjectService:
    def __init__(self, data) -> None:
        self.data = data
        self.album = {}
        self.album_cover = {}
        self.tracks = []

    def set_data(self):
        self.__set_album_data() 
        print(self.album)


    def validate_data(self):
        pass

    def __set_album_data(self):
        self.album = {
            "title": self.data.get(f'album[title]'),
            "bio": self.data.get(f'album[bio]'),
        }

