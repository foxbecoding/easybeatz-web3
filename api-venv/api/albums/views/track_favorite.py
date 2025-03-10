from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from albums.serializers import TrackFavoriteSerializer
from albums.models import Track, TrackFavorite
from core.mixins import ResponseMixin

class TrackFavoriteViewSet(viewsets.ViewSet, ResponseMixin):
    def get_permissions(self):
        permission_classes = [AllowAny]
        needs_auth = ['create', 'destroy']
        if self.action in needs_auth: permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request):
        track_id = request.data.get("track")
        track_qs = Track.objects.filter(tid=track_id).first()
        
        if not track_qs:
            return self.view_response("Track not found", None, status.HTTP_400_BAD_REQUEST)
        
        data = {"track": track_qs.pk, "user": request.user.pk}
        serializer = TrackFavoriteSerializer(data=data)
        if not serializer.is_valid():
            return self.view_response("Something went wrong, please try again", serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return self.view_response("Track added to favorites", str(track_id), status.HTTP_201_CREATED)

    def delete(self, request, pk=None):
        track_id = request.data.get("track")
        track_tids = TrackFavorite.objects.filter(user=request.user).values_list('track__tid', flat=True)

        if track_id not in list(track_tids):
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        track_ins = Track.objects.get(tid=track_id)

        track_favorite_ins = TrackFavorite.objects.get(track=track_ins, user=request.user)
        track_favorite_ins.delete()
        
        return Response(str(track_id), status=status.HTTP_200_OK)
