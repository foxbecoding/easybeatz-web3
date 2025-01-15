from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from ..serializers import StationSerializer

class StationViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def public_station(self, request, pk=None):
        is_owner = str(request.user) == str(pk)
        print(is_owner)
        return Response(pk, status=status.HTTP_200_OK)
