from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from ..serializers import Web3LoginNonceSerializer

class UserLoginNonceViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = Web3LoginNonceSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        nonce = serializer.save()

        return Response({"data": nonce.nonce}, status=status.HTTP_201_CREATED)
