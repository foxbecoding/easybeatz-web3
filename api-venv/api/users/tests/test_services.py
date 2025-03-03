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

    @patch("users.models.UserLoginNonce.objects.filter")
    @patch("users.utils.web3_login_message_generator")
    def test_invalid_message_verification(self, mock_msg_generator, mock_nonce_filter):
        """Test when the message verification fails"""
        mock_nonce_filter.return_value.last.return_value = MagicMock(nonce="123456")
        mock_msg_generator.return_value = "wrong_message"
        
        data = {"pubkey": "test_pubkey", "originalMessage": "message", "signedMessage": "signature"}
        service = Web3LoginService(data)
        
        response = service.run()
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"error": "Invalid signing message"}

