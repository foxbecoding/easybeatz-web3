from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from ..services import AlbumCreator, AlbumValidator, FormDataProcessor, TrackCreator, TrackValidator, TrackFormDataProcessor
from ..serializers import AlbumEditFormSerializer, AlbumWithTracksSerializer
from ..models import Album
from ..permissions import AlbumOwner
from stations.permissions import HasStation
from core.mixins import ResponseMixin

class AlbumViewSet(viewsets.ViewSet, ResponseMixin):
    def get_permissions(self):
        permission_classes = [AllowAny]
        needs_auth = ['update', 'add_track', 'create_with_tracks_and_relations']
        only_album_owner = ['update', 'add_track']
        if self.action in needs_auth:
            permission_classes = [IsAuthenticated, HasStation]
            if self.action in only_album_owner:
                permission_classes = [IsAuthenticated, HasStation, AlbumOwner]
        return [permission() for permission in permission_classes]

    def update(self, request, pk=None):
        album = Album.objects.get(aid=pk)
        serializer = AlbumEditFormSerializer(album, data=request.data)
        if not serializer.is_valid():
            return self.view_response("Failed to update album", serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return self.view_response("Album updated successfully", None, status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['post'])
    def add_track(self, request, pk=None):
        aid = pk
        processor = FormDataProcessor(request.data)
        processor.set_form_data()

        validator = TrackValidator(processor.tracks_form_data)
        if not validator.is_valid():
            return self.view_response("Invalid track details", validator.errors, status.HTTP_400_BAD_REQUEST)

        creator = TrackCreator(processor.tracks_form_data, aid)
        creator.create_track()

        return self.view_response("Track added successfully", None, status.HTTP_201_CREATED)

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
        aid = pk
        is_owner = Album.objects.filter(station__pk=request.user.pk, aid=aid).exists()
        qs = Album.albums.with_tracks_and_relations(pk)
        if not qs:
            return self.view_response("No album", None, status.HTTP_400_BAD_REQUEST) 
        serialized_data = AlbumWithTracksSerializer(qs, context={"is_owner": is_owner}).data
        return self.view_response(None, serialized_data, status.HTTP_200_OK)
