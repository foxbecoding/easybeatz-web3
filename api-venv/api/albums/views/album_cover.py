from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers import AlbumCoverEditSerializer
from ..models import Album, AlbumCover
from ..permissions import AlbumOwner
from stations.permissions import HasStation
from core.mixins import ResponseMixin
import logging

logger = logging.getLogger("albums")
class AlbumCoverViewSet(viewsets.ViewSet, ResponseMixin):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, HasStation]
        if self.action == 'update':
            permission_classes = [IsAuthenticated, HasStation, AlbumOwner]
        return [permission() for permission in permission_classes]

    def update(self, request, pk=None):
        album = Album.objects.get(aid=pk)
        album_cover = AlbumCover.objects.get(album=album)
        serializer = AlbumCoverEditSerializer(album_cover, data=request.data)
        if not serializer.is_valid():
            return self.view_response("Failed to update album cover", serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return self.view_response("Album cover updated successfully", None, status.HTTP_202_ACCEPTED)
