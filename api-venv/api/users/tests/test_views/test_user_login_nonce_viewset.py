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
        url = reverse("web3-login-nonce-list")
        response = client.post(url, valid_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("message") is None
        assert response.data.get("data") == {"message": "Generated Message"}

        # Check that a UserLoginNonce object was created
        assert UserLoginNonce.objects.count() == 1
        assert UserLoginNonce.objects.first().pubkey == valid_data["pubkey"]

# Test for invalid request
@pytest.mark.django_db
def test_create_user_login_nonce_invalid(client, invalid_data):
    """Test that creating a UserLoginNonce with invalid data returns a 400 Bad Request."""

    url = reverse("web3-login-nonce-list")
    response = client.post(url, invalid_data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data.get("message") is None
    assert response.data.get("data") is not None
    assert "pubkey" in response.data.get("data")
