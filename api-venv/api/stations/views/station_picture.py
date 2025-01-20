
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from ..serializers import  PublicStationSerializer
from ..models import StationPicture

class StationPictureViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        needs_auth = ['upload']
        if self.action in needs_auth: permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    @action(detail=False, methods=['post'])
    def upload(self, request):
        pass
