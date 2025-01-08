from rest_framework import serializers
from ..models import UserLoginNonce

class Web3LoginNonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLoginNonce
        fields = ['pubkey']
