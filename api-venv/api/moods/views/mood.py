
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Mood

class MoodViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request): 
        # serializer = StationSerializer(data=request.data, context={'request': request})
        # if not serializer.is_valid():
        #     return Response({"error": serializer.errors})
        # serializer.create(serializer.validated_data)
        # return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        pass

