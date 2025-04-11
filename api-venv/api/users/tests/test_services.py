import pytest
from unittest.mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APIRequestFactory
from users.services import Web3LoginService

@pytest.mark.django_db
class TestWeb3LoginService:
    
    @patch("users.models.UserLoginNonce.objects.filter")
    def test_no_nonce_found(self, mock_nonce_filter):
        """Test when no nonce is found for a wallet address"""
        mock_nonce_filter.return_value.last.return_value = None
        data = {"pubkey": "test_pubkey", "originalMessage": "message", "signedMessage": "signature"}

        factory = APIRequestFactory()
        request = factory.post("/auth/web3-login/", data, format='json')

        service = Web3LoginService(data, request)
        response = service.run()
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("message") == "No nonce found for this wallet address"
        assert response.data.get("data") is None

    @patch("users.models.UserLoginNonce.objects.filter")
    @patch("users.utils.web3_login_message_generator")
    def test_invalid_message_verification(self, mock_msg_generator, mock_nonce_filter):
        """Test when the message verification fails"""
        mock_nonce_filter.return_value.last.return_value = MagicMock(nonce="123456")
        mock_msg_generator.return_value = "wrong_message"
        
        data = {"pubkey": "test_pubkey", "originalMessage": "message", "signedMessage": "signature"}

        factory = APIRequestFactory()
        request = factory.post("/auth/web3-login/", data, format='json')

        service = Web3LoginService(data, request)
        
        response = service.run()
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("message") == "Invalid signing message"
        assert response.data.get("data") is None

    @patch("users.models.UserLoginNonce.objects.filter")
    @patch("users.utils.web3_login_message_generator")
    @patch("users.services.Web3LoginService._verify_message", return_value=True)
    @patch("users.services.Web3LoginService._verify_solana_signature", return_value=False)
    def test_invalid_signature_verification(self, mock_verify_signature, mock_verify_msg, mock_msg_generator, mock_nonce_filter):
        """Test when the Solana signature verification fails"""
        mock_nonce_filter.return_value.last.return_value = MagicMock(nonce="123456")
        mock_msg_generator.return_value = "message"
        
        data = {"pubkey": "test_pubkey", "originalMessage": "message", "signedMessage": "signature"}
        
        factory = APIRequestFactory()
        request = factory.post("/auth/web3-login/", data, format='json')

        service = Web3LoginService(data, request)
        
        response = service.run()
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("message") == "Verification failed"
        assert response.data.get("data") is None

    @patch("users.models.UserLoginNonce.objects.filter")
    @patch("users.utils.web3_login_message_generator")
    @patch("users.services.Web3LoginService._verify_message", return_value=True)
    @patch("users.services.Web3LoginService._verify_solana_signature", return_value=True)
    @patch("users.models.User.objects.get_or_create", return_value=(MagicMock(pubkey="test_pubkey"), True))
    @patch("albums.models.TrackFavorite.objects")
    @patch("rest_framework_simplejwt.tokens.RefreshToken.for_user", return_value=MagicMock(access_token="access_token"))
    @patch("users.signals.user_login_signal.web3_login_done.send")
    def test_successful_login(
        self, mock_signal_send, mock_refresh_token, mock_track_favorites, mock_get_or_create,  mock_verify_signature, mock_verify_message, mock_msg_generator, mock_nonce_filter
    ):
        """Test successful login"""
        mock_nonce_filter.return_value.last.return_value = MagicMock(nonce="123456")
        mock_msg_generator.return_value = "message"

        mock_filter = MagicMock()
        mock_filter.values_list.return_value = []
        mock_track_favorites.filter.return_value = mock_filter
        
        data = {"pubkey": "test_pubkey", "originalMessage": "message", "signedMessage": "signature"}
        service = Web3LoginService(data)
        
        response = service.run()
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("message") == "Logged in successfully!"
        assert response.data.get("data") == {"access_token": "access_token", "pubkey": "test_pubkey", "favorite_tracks": []}
        mock_signal_send.assert_called_once()
