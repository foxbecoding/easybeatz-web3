from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from albums.serializers import TrackFavoriteSerializer
from albums.models import Track

class TrackFavoriteViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        needs_auth = ['created']
        if self.action in needs_auth: permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request):
        track_id = request.data.get("track")
        track_qs = Track.objects.filter(tid=track_id).first()
        
        if not track_qs:
            return Response({"errors": "Track not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data = {"track": track_qs.pk, "user": request.user.pk}
        serializer = TrackFavoriteSerializer(data=data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(str(track_id), status=status.HTTP_201_CREATED)
