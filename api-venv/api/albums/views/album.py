from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from ..services import AlbumCreator, AlbumValidator, FormDataProcessor
from stations.permissions import HasStation
from ..serializers import AlbumWithTracksSerializer
from ..models import Album

class AlbumViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        needs_auth = ['create_with_tracks_and_relations']
        if self.action in needs_auth: permission_classes = [IsAuthenticated, HasStation]
        return [permission() for permission in permission_classes]

