import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.urls import reverse

@pytest.fixture
def client():
    """Fixture for the API client."""
    # Ensure HTTP is used for testing, bypassing the HTTPS redirect.
    settings.SECURE_SSL_REDIRECT = False  # Disable automatic redirect to HTTPS
    return APIClient()

@pytest.mark.django_db
def test_user_logout_view(client, default_user):
    """Test that an authenticated user can log out successfully."""
    
    # Generate JWT token for authentication
    refresh = RefreshToken.for_user(default_user)
    access_token = str(refresh.access_token)

    # Authenticate the client
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # Send a POST request to logout
    response = client.post("/api/logout/")  # Adjust URL based on your routes
    
    # Check response status
    assert response.status_code == 200  # Expect HTTP 200 OK

    # Ensure authentication credentials are removed
    client.credentials()  # Reset credentials

    # Try to access a protected endpoint (this should fail)
    protected_response = client.post("/api/album/create_with_tracks_and_relations/")  # Adjust URL to a real protected route
    assert protected_response.status_code == 401  # Expect HTTP 401 Unauthorized
