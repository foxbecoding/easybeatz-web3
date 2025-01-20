
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from ..serializers import StationPictureSerializer
from ..models import Station, StationPicture
from users.models import User

class StationPictureViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        needs_auth = ['upload']
        if self.action in needs_auth: permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    @action(detail=False, methods=['post'])
    def upload(self, request):
        # check if user has station
        user = User.objects.filter(pubkey=str(request.user)).first()
        station = Station.objects.filter(pk=user.pk).first()

        if not station:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        request.data['station'] = station
        serializer = StationPictureSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        
        serializer.save()

        return Response("Picture uploaded successfully", status=status.HTTP_200_OK)
