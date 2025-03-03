import pytest
from unittest.mock import patch, MagicMock
from rest_framework import status
from users.services import Web3LoginService

@pytest.mark.django_db
class TestWeb3LoginService:
    
    @patch("users.models.UserLoginNonce.objects.filter")
    def test_no_nonce_found(self, mock_nonce_filter):
        """Test when no nonce is found for a wallet address"""
        mock_nonce_filter.return_value.last.return_value = None
        data = {"pubkey": "test_pubkey", "originalMessage": "message", "signedMessage": "signature"}
        service = Web3LoginService(data)
        
        response = service.run()
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"error": "No nonce found for this wallet address"}

