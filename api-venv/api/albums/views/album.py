from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from ..services import AlbumCreator, AlbumValidator, FormDataProcessor
from stations.permissions import HasStation
from ..serializers import AlbumWithTracksSerializer
from ..models import Album
from core.mixins import ResponseMixin

class AlbumViewSet(viewsets.ViewSet, ResponseMixin):
    def get_permissions(self):
        permission_classes = [AllowAny]
        needs_auth = ['create_with_tracks_and_relations']
        if self.action in needs_auth: permission_classes = [IsAuthenticated, HasStation]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def create_with_tracks_and_relations(self, request):
        processor = FormDataProcessor(request.data)
        processor.set_form_data()

        validator = AlbumValidator(processor.album_form_data, processor.tracks_form_data)
        if not validator.is_valid():
            return self.view_response("Invalid album details", validator.errors, status.HTTP_400_BAD_REQUEST)

        creator = AlbumCreator(processor.album_form_data, processor.tracks_form_data, request.user)
        creator.create_album()

        return self.view_response("Album created", None, status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def retrieve_with_tracks_and_relations(self, request, pk=None):
        qs = Album.albums.with_tracks_and_relations(pk)
        if not qs:
            return self.view_response("No album", None, status.HTTP_400_BAD_REQUEST) 
        serialized_data = AlbumWithTracksSerializer(qs).data
        return self.view_response(None, serialized_data, status.HTTP_200_OK)
