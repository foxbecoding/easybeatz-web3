from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from ..models import Track
from ..permissions import TrackOwner
from ..serializers import TrackEditFormSerializer, TrackPageSerializer
from stations.permissions import HasStation
from core.mixins import ResponseMixin
import logging

logger = logging.getLogger("albums")

class TrackViewSet(viewsets.ViewSet, ResponseMixin):
    def get_permissions(self):
        permission_classes = [AllowAny]
        needs_auth = ['update']
        if self.action in needs_auth:
            permission_classes = [IsAuthenticated, HasStation]
            if self.action == 'update':
                permission_classes = [IsAuthenticated, HasStation, TrackOwner]
        return [permission() for permission in permission_classes]


    @action(detail=True, methods=['get'])
    def track_page(self, request, pk=None):
        tid = pk
        qs = Track.tracks.track_page(tid)
        if not qs:
            return self.view_response("Track page does not exists", None, status.HTTP_404_NOT_FOUND)
        serialized_data = TrackPageSerializer(qs).data
        return self.view_response(None, serialized_data, status.HTTP_200_OK)


    def update(self, request, pk=None):
        track = Track.objects.get(tid=pk)
        serializer = TrackEditFormSerializer(track, data=request.data)
        if not serializer.is_valid():
            return self.view_response("Failed to update track", serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return self.view_response("Track updated successfully", None, status.HTTP_202_ACCEPTED)
