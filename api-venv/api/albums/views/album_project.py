from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from ..services import AlbumProjectService, AlbumFormService
from stations.permissions import HasStation
from ..serializers import AlbumProjectSerializer
from ..models import Album

class AlbumProjectViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        needs_auth = ['create']
        if self.action in needs_auth: permission_classes = [IsAuthenticated, HasStation]
        return [permission() for permission in permission_classes]

    def create(self, request):
        service = AlbumProjectService(request.data)
        service.set_form_data()
        if not service.is_form_data_valid():
            return Response({"errors": service.errors})
        service.save(request)
        return Response("Album created", status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        album_qs = Album.objects.with_tracks_and_relations(pk)
        if not album_qs:
            return Response({"error": "No Project"}, status=status.HTTP_404_NOT_FOUND) 
        serialized_data = AlbumProjectSerializer(album_qs).data
        return Response(serialized_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def validate_album_form(self, request):
        service = AlbumFormService(request.data)
        if not service.is_valid():
            return Response({"errors": service.errors})
        return Response(None, status=status.HTTP_200_OK)
