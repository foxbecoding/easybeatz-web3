from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Track
from ..permissions import TrackOwner
from ..serializers import TrackEditFormSerializer
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

    def update(self, request, pk=None):
        track = Track.objects.get(tid=pk)
        serializer = TrackEditFormSerializer(track, data=request.data)
        if not serializer.is_valid():
            return self.view_response("Failed to update track", serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return self.view_response("Track updated successfully", None, status.HTTP_202_ACCEPTED)
