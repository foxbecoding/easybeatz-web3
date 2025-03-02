import pytest
from users.models import UserLoginNonce
from users.tests.factories import UserLoginNonceFactory

@pytest.mark.django_db
def test_create_user_login_nonce():
    """
    Ensure a UserLoginNonce model can be created successfully.
    """
    user_login_nonce = UserLoginNonce.objects.create(
        pubkey="D3c6JWSDHXsUCHf8uuQ9raYmDnbnCHTvb5FHHvNrdjPF"
    )
    assert user_login_nonce.pk is not None  # Check if saved to the DB
    assert user_login_nonce.nonce is not None  # Ensure nonce is generated
    assert len(user_login_nonce.nonce) == 36  # Validate nonce format (UUID)

@pytest.mark.django_db
def test_user_login_nonce_factory_creates_valid_instance():
    """
    Ensure that the UserLoginNonceFactory correctly creates a UserLoginNonce instance.
    """
    user_login_nonce = UserLoginNonceFactory()
    assert user_login_nonce.pk is not None
    assert user_login_nonce.pubkey is not None
    assert user_login_nonce.nonce is not None
    assert len(user_login_nonce.nonce) == 36  # Validate UUID length

@pytest.mark.django_db
def test_user_login_nonce_with_default_fixture(default_user_login_nonce):
    """
    Test that the default_user_login_nonce fixture creates a valid instance.
    """
    assert default_user_login_nonce.pk is not None
    assert default_user_login_nonce.pubkey == "D3c6JWSDHXsUCHf8uuQ9raYmDnbnCHTvb5FHHvNrdjPF"
    assert default_user_login_nonce.nonce is not None
    assert len(default_user_login_nonce.nonce) == 36  # Validate UUID format
