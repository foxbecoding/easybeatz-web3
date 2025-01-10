from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from solders.pubkey import Pubkey
from solders.signature import Signature
from ..models import User, UserLogin, UserLoginNonce 
from ..serializers import Web3LoginSerializer

class UserLoginViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes] 

    def create(self, request):
        serializer = Web3LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        pubkey = serializer.validated_data['pubkey']
        message = serializer.validated_data['originalMessage']
        nonce = UserLoginNonce.objects.filter(pubkey=pubkey).last()

        if not nonce:
            return Response({"error": "No nonce found for this wallet address"}, status=status.HTTP_400_BAD_REQUEST)

        if not self.verify_nonce(message, nonce.nonce):
            return Response({"error": "Invalid message or nonce"}, status=status.HTTP_400_BAD_REQUEST)

        if not self.verify_solana_signature(serializer.validated_data):
            return Response({"error": "Verification failed"}, status=status.HTTP_400_BAD_REQUEST)

        user = self.find_or_create_user(pubkey)
        access_token = self.authenticate_user(user)

        return Response({"access_token": access_token, "pubkey": user.pubkey, "username": user.username}, status=status.HTTP_200_OK)

    
