from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from ..serializers import Web3LoginSerializer
from ..services import Web3LoginService


class UserLoginViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes] 

    def create(self, request):
        serializer = Web3LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        service = Web3LoginService(serializer.validated_data)
        return service.run()
