from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from users.models import User
from stations.models import Station


class AlbumProjectService:
    def __init__(self, data) -> None:
        self.data = data
        self.album = {}
        self.tracks = []

    def run(self):
        print(self.data)

