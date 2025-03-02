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

