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

    def get_permissions(self):
        permission_classes = [AllowAny]
        needs_auth = ['created']
        if self.action in needs_auth: permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request):
        pass
