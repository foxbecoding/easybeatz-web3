import pytest
import uuid
from users.models import User, UserLogin, UserLoginNonce

@pytest.fixture
def default_user(db):
    """
    A static User fixture. This user can be used across multiple tests.
    """
    return User.objects.create(
        pubkey="D3c6JWSDHXsUCHf8uuQ9raYmDnbnCHTvb5FHHvNrdjPF",
        email="john@example.com"
    )

@pytest.fixture
def default_user_login(db, default_user):
    """
    A static UserLogin fixture. This login entry can be used across multiple tests.
    """
    return UserLogin.objects.create(user=default_user)

@pytest.fixture
def default_user_login_nonce(db):
    """
    A fixture to create a default UserLoginNonce instance.
    """
    return UserLoginNonce.objects.create(
        pubkey="D3c6JWSDHXsUCHf8uuQ9raYmDnbnCHTvb5FHHvNrdjPF"
    )
