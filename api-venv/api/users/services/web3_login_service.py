from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from solders.pubkey import Pubkey
from solders.signature import Signature
from ..models import User, UserLogin, UserLoginNonce
from stations.models import Station

class Web3LoginService:
    def __init__(self, data) -> None:
        self.validated_data = data
        self.pubkey = data["pubkey"]
        self.message = data["originalMessage"]
        self.signature = data["signedMessage"]

    def run(self) -> Response:
        nonce = UserLoginNonce.objects.filter(pubkey=self.pubkey).last()

        if not nonce:
            return Response({"error": "No nonce found for this wallet address"}, status=status.HTTP_400_BAD_REQUEST)

        if not self.__verify_nonce(self.message, nonce.nonce):
            return Response({"error": "Invalid message or nonce"}, status=status.HTTP_400_BAD_REQUEST)

        if not self.__verify_solana_signature(self.validated_data):
            return Response({"error": "Verification failed"}, status=status.HTTP_400_BAD_REQUEST)

        user = self.__find_or_create_user(self.pubkey)
        access_token = self.__authenticate_user(user)
        station = self.__get_station(user)
        self.__save_user_login(user)

        return Response({"access_token": access_token, "pubkey": user.pubkey,  "station": station}, status=status.HTTP_200_OK)

    def __verify_solana_signature(self, data) -> bool:
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

    def __verify_nonce(self, message: str, nonce: str) -> bool:
        # Verify that the message contains the expected nonce
        return nonce in message

    def __find_or_create_user(self, pubkey: str) -> User:
        user, created = User.objects.get_or_create(pubkey=pubkey)

        # If the user wasn't created (it already exists), you can return the existing user
        if not created:
            return user
        return user

    def __authenticate_user(self, user: User) -> str:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return access_token

    def __save_user_login(self, user: User) -> None:
        user_login = UserLogin(user = user)
        user_login.save()

    def __get_station(self, user: User) -> Station | None :
        return Station.objects.filter(pk=user.pk).first() or None
        
