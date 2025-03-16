from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..models import Mood
from ..serializers import MoodSerializer
from core.mixins import ResponseMixin

class MoodViewSet(viewsets.ViewSet, ResponseMixin):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request):
        query_set = Mood.objects.all()
        serializer = MoodSerializer(query_set, many=True)
        data = serializer.data
        return self.view_response(None, data, status.HTTP_200_OK)
