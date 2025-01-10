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
       pass 
