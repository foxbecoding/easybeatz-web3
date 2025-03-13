import pytest
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from users.models import UserLoginNonce
from django.conf import settings
from django.urls import reverse

@pytest.fixture
def client():
    """Fixture for the API client."""
    # Ensure HTTP is used for testing, bypassing the HTTPS redirect.
    settings.SECURE_SSL_REDIRECT = False  # Disable automatic redirect to HTTPS
    return APIClient()

@pytest.fixture
def valid_data():
    """Fixture for valid data to send to the view."""
    return {
        "pubkey": "D3c6JWSDHXsUCHf8uuQ9raYmDnbnCHTvb5FHHvNrdjPF"
    }

@pytest.fixture
def invalid_data():
    """Fixture for invalid data."""
    return {
        "invalid_field": "some_value"
    }

# Test for valid request
@pytest.mark.django_db
def test_create_user_login_nonce_success(client, valid_data):
    """Test that creating a UserLoginNonce with valid data works."""
    with patch("users.views.login_nonce.web3_login_message_generator") as mock_message_generator:
        mock_message_generator.return_value = "Generated Message"

        # Send POST request
        response = client.post("/api/web3-login-nonce/", valid_data, format="json")

        # Check that the response status is 201 Created
        assert response.status_code == status.HTTP_201_CREATED

        # Check that the correct message is returned
        assert response.data["message"] == "Generated Message"
        # assert response.data["message"] == expected_message

        # Check that a UserLoginNonce object was created
        assert UserLoginNonce.objects.count() == 1
        assert UserLoginNonce.objects.first().pubkey == valid_data["pubkey"]

# Test for invalid request
@pytest.mark.django_db
def test_create_user_login_nonce_invalid(client, invalid_data):
    """Test that creating a UserLoginNonce with invalid data returns a 400 Bad Request."""
    response = client.post("/api/web3-login-nonce/", invalid_data, format="json")

    # Check that the response status is 400 Bad Request
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Ensure that error details are returned
    assert "error" in response.data
    assert "pubkey" in response.data["error"]
