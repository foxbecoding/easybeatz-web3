from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from ..services import AlbumProjectService
from users.models import User
from stations.models import Station

class AlbumProjectViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request):
        # Check if user has a station
        user = User.objects.filter(pubkey=str(request.user)).first()
        station = Station.objects.filter(pk=user.pk).first()
        if not station:
            return Response("Not Authorized", status=status.HTTP_401_UNAUTHORIZED)

        # run service
        service = AlbumProjectService(request.data)
        service.set_form_data()
        if not service.is_form_data_valid():
            return Response({"errors": service.errors})
        service.save(station)
        return Response("Easy Beatz", status=status.HTTP_200_OK)
