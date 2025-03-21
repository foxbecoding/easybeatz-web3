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

