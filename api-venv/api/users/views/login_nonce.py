from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from ..serializers import Web3LoginNonceSerializer
from ..utils import web3_login_message_generator

class UserLoginNonceViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = Web3LoginNonceSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({ "error": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

        nonce = serializer.save()
        message = web3_login_message_generator(nonce.nonce, request.data.get("pubkey"))

        return Response({"message": message}, status=status.HTTP_201_CREATED)
