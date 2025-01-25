from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from users.models import User
from stations.models import Station


class AlbumProjectService:
    def __init__(self, data) -> None:
        self.form_data = data
        self.album = {}
        self.album_cover = {}
        self.tracks = []
        self.__set_form_data()


    def __set_form_data(self):
        self.__set_album_data() 
        print(self.album)


    def __set_album_data(self):
        self.album = {
            "title": self.form_data.get(f'album[title]'),
            "bio": self.form_data.get(f'album[bio]'),
        }

    def is_form_data_valid(self) -> bool:
        return False 

