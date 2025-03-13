from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from ..permissions import HasStation
from ..serializers import StationPictureSerializer
from ..models import Station, StationPicture
from users.models import User
from core.mixins import ResponseMixin

class StationPictureViewSet(viewsets.ViewSet, ResponseMixin):
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
            serializer = StationPictureSerializer(data=request.data, context={"station": station})
        else:
            serializer = StationPictureSerializer(station_picture, data=request.data)
        if not serializer.is_valid():
            return self.view_response("Invalid image format", serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return self.view_response("Picture uploaded successfully!", None, status.HTTP_200_OK)
