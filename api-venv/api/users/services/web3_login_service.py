from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from solders.pubkey import Pubkey
from solders.signature import Signature
from ..models import User, UserLoginNonce
from ..signals.user_login_signal import web3_login_done
from ..utils import web3_login_message_generator
from albums.models import TrackFavorite

class Web3LoginService:
    def __init__(self, data) -> None:
        self.validated_data = data
        self.pubkey = data.get("pubkey")
        self.message = data.get("originalMessage")
        self.signature = data.get("signedMessage")

    def run(self):
        nonce = self._get_nonce()

        if not nonce:
            return Response({"error": "No nonce found for this wallet address"}, status=status.HTTP_400_BAD_REQUEST)

        if not self._verify_message(nonce.nonce):
            return Response({"error": "Invalid signing message"}, status=status.HTTP_400_BAD_REQUEST)

        if not self._verify_solana_signature():
            return Response({"error": "Verification failed"}, status=status.HTTP_400_BAD_REQUEST)

        user = self._find_or_create_user()
        access_token = self._authenticate_user(user['user'])
        self._save_user_login(user['user'])
        return Response({"access_token": access_token, "pubkey": user['user'].pubkey, "favorite_tracks": user['track_tids']}, status=status.HTTP_200_OK)

    def _get_nonce(self):
        return UserLoginNonce.objects.filter(pubkey=self.pubkey).last()

    def _verify_message(self, nonce: str):
        message = web3_login_message_generator(nonce, self.pubkey)
        return message == self.message

    def _verify_solana_signature(self):
        message = self.message

        try:
            # Parse the public key
            pubkey = Pubkey.from_string(self.pubkey)

            # Decode the signature from base58
            signature = Signature.from_bytes(self.signature)

            # Convert the message into bytes (if it's a string)
            if isinstance(message, str):
                message = message.encode("utf-8")

            # Verify the signature
            is_valid = signature.verify(pubkey, message)
            return is_valid

        except Exception as e:
            print(f"Verification failed: {e}")
            return False

    def _find_or_create_user(self):
        user, _ = User.objects.get_or_create(pubkey=self.pubkey)
        track_tids = TrackFavorite.objects.filter(user=user).values_list('track__tid', flat=True)
        return {"user": user, "track_tids": list(track_tids) }

    def _authenticate_user(self, user: User) -> str:
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def _save_user_login(self, user: User) -> None:
        web3_login_done.send(self.__class__, user=user)
