from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from solders.pubkey import Pubkey
from solders.signature import Signature
from ..models import User, UserLogin, UserLoginNonce
from ..serializers import Web3LoginSerializer

class Web3LoginService:
    def __init__(self, data) -> None:
        self.validated_data = data
        self.pubkey = data["pubkey"]
        self.message = data["originalMessage"]
        self.signature = data["signature"]

    def run(self):
       nonce = UserLoginNonce.objects.filter(pubkey=self.pubkey).last()

        if not nonce:
            return Response({"error": "No nonce found for this wallet address"}, status=status.HTTP_400_BAD_REQUEST)

        if not self.verify_nonce(self.message, nonce.nonce):
            return Response({"error": "Invalid message or nonce"}, status=status.HTTP_400_BAD_REQUEST)

        if not self.verify_solana_signature(self.validated_data):
            return Response({"error": "Verification failed"}, status=status.HTTP_400_BAD_REQUEST)

        user = self.find_or_create_user(self.pubkey)
        access_token = self.authenticate_user(user)
        
        return Response({"access_token": access_token, "pubkey": user.pubkey, "username": user.username}, status=status.HTTP_200_OK)
