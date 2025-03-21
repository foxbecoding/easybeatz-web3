from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Track, TrackExclusivePrice
from ..permissions import TrackOwner
from ..serializers import CreateTrackExclusivePriceSerializer, TrackExclusivePriceEditFormSerializer
from stations.permissions import HasStation
from core.mixins import ResponseMixin
import logging

logger = logging.getLogger("albums")

class TrackExclusivePriceViewSet(viewsets.ViewSet, ResponseMixin):
    def get_permissions(self):
        permission_classes = [AllowAny]
        needs_auth = ['update', 'destroy']
        track_owner_actions = ['update', 'destroy']
        if self.action in needs_auth:
            permission_classes = [IsAuthenticated, HasStation]
            if self.action in track_owner_actions:
                permission_classes = [IsAuthenticated, HasStation, TrackOwner]
        return [permission() for permission in permission_classes]

    def update(self, request, pk=None):
        track_tid = pk
        track_exclusive_price = TrackExclusivePrice.objects.filter(track__tid=track_tid).first()
        # Create if not present
        if not track_exclusive_price:
            track = Track.objects.get(tid=track_tid)
            request_data = {"track": str(track.pk), "value": request.data['value']}
            serializer = CreateTrackExclusivePriceSerializer(data=request_data)
            if not serializer.is_valid():
                return self.view_response("Failed to add exclusive price", serializer.errors, status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return self.view_response("Exclusive price added successfully", None, status.HTTP_201_CREATED)

        # Update if present
        serializer = TrackExclusivePriceEditFormSerializer(track_exclusive_price, data=request.data)
        if not serializer.is_valid():
            return self.view_response("Failed to update exclusive price", serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return self.view_response("Exclusive price updated successfully", None, status.HTTP_202_ACCEPTED)

