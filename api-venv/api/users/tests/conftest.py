import pytest
import uuid
from users.models import User, UserLogin, UserLoginNonce

@pytest.fixture
def default_user(db):
    """
    A static user fixture. This user can be used across multiple tests.
    """
    return User.objects.create(
        pubkey="D3c6JWSDHXsUCHf8uuQ9raYmDnbnCHTvb5FHHvNrdjPF",
        email="john@example.com"
    )
