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

    def retrieve(self, request, pk=None):
        return Response(pk, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = StationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        return Response({"data": data}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def public_station(self, request, pk=None):
        return Response(pk, status=status.HTTP_200_OK)
