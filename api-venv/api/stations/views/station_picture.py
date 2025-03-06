from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from ..permissions import HasStation
from ..serializers import StationPictureSerializer
from ..models import Station, StationPicture
from users.models import User

class StationPictureViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        needs_auth = ['upload']
        if self.action in needs_auth: permission_classes = [IsAuthenticated, HasStation]
        return [permission() for permission in permission_classes]


    @action(detail=False, methods=['post'])
    def upload(self, request):
        user = User.objects.filter(pubkey=str(request.user)).first()
        station = Station.objects.filter(pk=user.pk).first()
        station_picture = StationPicture.objects.filter(pk=station.pk).first()
        if not station_picture:
            request.data['station'] = station
            serializer = StationPictureSerializer(data=request.data)
        else:
            serializer = UpdateStationPictureSerializer(station_picture, data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors})
        serializer.save()
        return Response("Picture uploaded successfully", status=status.HTTP_200_OK)
