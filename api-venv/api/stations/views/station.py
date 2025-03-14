from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from ..serializers import StationSerializer, StationWithAlbumsAndRelationsSerializer
from ..models import Station
from ..decorators import check_user_pubkey
from core.mixins import ResponseMixin

class StationViewSet(viewsets.ViewSet, ResponseMixin):
    def get_permissions(self):
        permission_classes = [AllowAny]
        needs_auth = ['partial_update', 'update', 'create', 'has_station', 'retrieve']
        if self.action in needs_auth: permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request): 
        serializer = StationSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return self.view_response("Failed to create station", serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        return self.view_response("Station created successfully!", None, status.HTTP_201_CREATED)

    @check_user_pubkey
    def retrieve(self, request, pk=None):
        qs = Station.objects.select_related("user").get(user__pubkey=str(pk))
        serialized_station = StationSerializer(qs).data
        return Response(serialized_station, status=status.HTTP_200_OK)

    @check_user_pubkey
    def update(self, request, pk=None):
        qs = Station.objects.select_related("user").get(user__pubkey=str(pk))
        serializer = StationSerializer(qs, data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors})
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def has_station(self, request):
        user_pubkey = str(request.user)
        qs_exists = Station.objects.select_related("user").filter(user__pubkey=user_pubkey).exists()
        return Response(qs_exists, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def retrieve_with_albums_and_relations(self, request, pk=None):
        user_pubkey = str(pk)
        is_owner = False
        if request.user is not None:
            is_owner = str(request.user) == user_pubkey
        qs = Station.stations.with_albums_and_relations(user_pubkey)

        if not qs:
            return Response({"error": "No Station", "is_owner": is_owner}, status=status.HTTP_404_NOT_FOUND) 

        serialized_data = StationWithAlbumsAndRelationsSerializer(qs, context={"is_owner": is_owner}).data
        return Response(serialized_data, status=status.HTTP_200_OK)


