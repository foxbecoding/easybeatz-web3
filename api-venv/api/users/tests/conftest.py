import pytest
from users.models import User

@pytest.fixture
def default_user(db):
    """
    A static user fixture. This user can be used across multiple tests.
    """
    return User.objects.create(
        pubkey="D3c6JWSDHXsUCHf8uuQ9raYmDnbnCHTvb5FHHvNrdjPF",
        email="john@example.com"
    )
