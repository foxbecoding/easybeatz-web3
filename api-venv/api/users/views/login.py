from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from solders.pubkey import Pubkey
from solders.signature import Signature
from ..models import User, UserLogin 
from ..serializers import Web3LoginSerializer

class UserLoginViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def verify_solana_signature(self, data):
        signature_bytes = data['signedMessage']
        pubkey_str = data['pubkey']
        message = data['originalMessage']

        try:
            # Parse the public key
            pubkey = Pubkey.from_string(pubkey_str)

            # Decode the signature from base58
            signature = Signature.from_bytes(signature_bytes)

            # Convert the message into bytes (if it's a string)
            if isinstance(message, str):
                message = message.encode("utf-8")

            # Verify the signature
            is_valid = signature.verify(pubkey, message)
            return is_valid

        except Exception as e:
            print(f"Verification failed: {e}")
            return False

    def find_or_create_user(self, pubkey):
        user, created = User.objects.get_or_create(pubkey=pubkey)
        
        # If the user wasn't created (it already exists), you can return the existing user
        if not created:
            return user
        return user

    def authenticate_user(self):
        pass

    def create(self, request):
        serializer = Web3LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not self.verify_solana_signature(serializer.validated_data):
            return Response({"message": "Verification failed"}, status=status.HTTP_400_BAD_REQUEST)

        pubkey = serializer.validated_data['pubkey']

        user = self.find_or_create_user(pubkey)

        print(user)

        # return Response({"message": "Success", "data": validated_data}, status=status.HTTP_200_OK)
        # print(request.data["pubkey"])
        return Response("fox")
