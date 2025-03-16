from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..models import Genre
from ..serializers import GenreSerializer
from core.mixins import ResponseMixin

class GenreViewSet(viewsets.ViewSet, ResponseMixin):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request):
        query_set = Genre.objects.all()
        serializer = GenreSerializer(query_set, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

