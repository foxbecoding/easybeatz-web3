from django.db.models import Count, Prefetch, Sum
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from ..models import Album, Track

class AlbumViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        needs_auth = ['created']
        if self.action in needs_auth: permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=None):
        album_qs = Album.objects.prefecth_related(
            Prefetch(
                "tracks",
                queryset=Track.objects
                .only("bpm", "duration", "tid", "title")
            )
        )
        
        if not album_qs:
            return Response({"error": "No Station", "is_owner": is_owner}, status=status.HTTP_404_NOT_FOUND) 
