import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.response import Response
from unittest.mock import patch
from django.conf import settings

@pytest.fixture
def client():
    """Fixture for the API client."""
    settings.SECURE_SSL_REDIRECT = False  # Disable automatic redirect to HTTPS
    return APIClient()

@pytest.fixture
def valid_data():
    """Fixture for valid data to send to the view."""
    return {
        "pubkey": "D3c6JWSDHXsUCHf8uuQ9raYmDnbnCHTvb5FHHvNrdjPF",
        "signedMessage": {  # Correct format for BinaryField
            "type": "Buffer",
            "data": [100, 200, 150, 50, 255, 30]  # Example byte values
        },
        "originalMessage": "Mocked Original Message",  # Must match web3_login_message_generator
    }

@pytest.fixture
def invalid_data():
    """Fixture for invalid data."""
    return {
        "pubkey": "D3c6JWSDHXsUCHf8uuQ9raYmDnbnCHTvb5FHHvNrdjPF",
        # Missing signature field or invalid format
    }

# Test for valid request
@pytest.mark.django_db
def test_create_user_login_valid(client, valid_data):
    """Test that valid data creates a user login and returns the correct response."""

    with patch("users.views.login.Web3LoginService") as MockService:
        # Mock the service instance
        mock_service_instance = MockService.return_value
        mock_service_instance.run.return_value = Response({
            "access_token": "mocked_access_token",
            "pubkey": valid_data["pubkey"]
        })

        # Send POST request to the view
        response = client.post("/api/web3-login/", valid_data, format="json")

        # Ensure the response status is 200 OK
        assert response.status_code == status.HTTP_200_OK

        # Validate the response structure
        assert response.data["access_token"] == "mocked_access_token"
        assert response.data["pubkey"] == valid_data["pubkey"]

        # Ensure the mock service was called correctly
        mock_service_instance.run.assert_called_once()
   
        MockService.return_value.run.assert_called_once()

# Test for invalid request
@pytest.mark.django_db
def test_create_user_login_invalid(client, invalid_data):
    """Test that invalid data returns a 400 Bad Request with error details."""

    # Send POST request to the view with invalid data
    response = client.post("/api/web3-login/", invalid_data, format="json")

    # Check that the response status is 400 Bad Request
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Ensure that error details are returned
    assert "error" in response.data
    assert "signedMessage" in response.data["error"]

