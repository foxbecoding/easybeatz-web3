from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from ..serializers import StationSerializer, PublicStationSerializer
from users.models import User
from ..models import Station, StationPicture
from datetime import datetime

class StationViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        needs_auth = ['partial_update', 'update', 'create', 'has_station', 'retrieve']
        if self.action in needs_auth: permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request): 
        serializer = StationSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({"error": serializer.errors})
        serializer.create(serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        if str(request.user) != str(pk):
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.filter(pubkey=str(pk)).first()
        station = Station.objects.get(pk=user.pk) 
        serialized_station = StationSerializer(station).data
        return Response(serialized_station, status=status.HTTP_200_OK)


    def update(self, request, pk=None):
        if str(request.user) != str(pk):
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.filter(pubkey=str(request.user)).first()
        station_ins = Station.objects.get(pk=str(user.pk))
        serializer = StationSerializer(station_ins, data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors})
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def has_station(self, request):
        user = User.objects.filter(pubkey=str(request.user)).first()
        station_exists = Station.objects.filter(pk=user.pk).exists()
        return Response(station_exists, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def public_station(self, request, pk=None):
        # Check if station exists
        is_owner = str(request.user) == str(pk)
        user = User.objects.filter(pubkey=str(pk)).first()
        station_exists = Station.objects.filter(pk=user.pk).first()
        if not user or not station_exists:
            return Response({"error": "No Station", "is_owner": is_owner}, status=status.HTTP_404_NOT_FOUND)

        station = Station.objects.get(pk=user.pk) 
        serialized_station = PublicStationSerializer(station).data
        serialized_station['is_owner'] = is_owner
        created_date = datetime.fromisoformat(serialized_station['created'].replace("Z", "+00:00"))
        serialized_station['created'] = created_date.year
        picture = StationPicture.objects.get(pk=serialized_station.get('picture'))
        serialized_station['picture'] = str(picture.picture)
        return Response(serialized_station, status=status.HTTP_200_OK)


