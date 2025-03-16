from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from ..serializers import Web3LoginNonceSerializer
from ..utils import web3_login_message_generator
from core.mixins import ResponseMixin

class UserLoginNonceViewSet(viewsets.ViewSet, ResponseMixin):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = Web3LoginNonceSerializer(data=request.data)

        if not serializer.is_valid():
            return self.view_response(None, serializer.errors, status.HTTP_400_BAD_REQUEST)

        nonce = serializer.save()
        message = web3_login_message_generator(nonce.nonce, request.data.get("pubkey"))

        return self.view_response(None, {"message": message}, status.HTTP_201_CREATED)
