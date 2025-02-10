from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Mood
from ..serializers import MoodSerializer

class MoodViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request):
        query_set = Mood.objects.all()
        serializer = MoodSerializer(query_set, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
