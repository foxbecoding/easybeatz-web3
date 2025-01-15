from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from ..serializers import StationSerializer
from users.models import User
from ..models import Station
from datetime import datetime

class StationViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def public_station(self, request, pk=None):
        # Check if station exists
        user = User.objects.filter(pubkey=str(pk)).first()
        if not user:
            return Response({"error": "No Station"}, status=status.HTTP_404_NOT_FOUND)

        station = Station.objects.get(pk=user.pk) 
        serialized_station = StationSerializer(station).data
        is_owner = str(request.user) == str(pk)
        serialized_station['is_owner'] = is_owner
        created_date = datetime.fromisoformat(serialized_station['created'].replace("Z", "+00:00"))
        serialized_station['created'] = created_date.year
        # serialized_station['created'] = serialized_station['created'].month
        return Response(serialized_station, status=status.HTTP_200_OK)
