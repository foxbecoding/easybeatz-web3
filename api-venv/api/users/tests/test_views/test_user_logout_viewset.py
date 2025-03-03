import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

@pytest.fixture
def client():
    """Fixture for the API client."""
    # Ensure HTTP is used for testing, bypassing the HTTPS redirect.
    settings.SECURE_SSL_REDIRECT = False  # Disable automatic redirect to HTTPS
    return APIClient()

