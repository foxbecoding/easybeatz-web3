import pytest
from users.models import User
from users.tests.factories import UserFactory

@pytest.mark.django_db
def test_create_user():
    """
    Ensure a User model can be created successfully.
    """
    user = User.objects.create(
        pubkey="D3c6JWSDHXsUCHf8uuQ9raYmDnbnCHTvb5FHHvNrdjPF",
        email="test@example.com"
    )
    assert user.pk is not None  # Check if saved to the DB


@pytest.mark.django_db
def test_user_factory_creates_valid_user():
    """
    Ensure that the UserFactory correctly creates a User instance.
    """
    user = UserFactory()
    assert user.pk is not None
    assert user.pubkey is not None

@pytest.mark.django_db
def test_user_str_returns_pubkey():
    """
    Test that the __str__ method returns the pubkey.
    """
    user = UserFactory(pubkey="unique_pubkey")
    assert str(user) == "unique_pubkey"

@pytest.mark.django_db
def test_user_with_default_fixture(default_user):
    """
    Test that the default_user fixture creates a user with the expected data.
    """
    # Check that __str__ returns the pubkey.
    assert str(default_user) == "D3c6JWSDHXsUCHf8uuQ9raYmDnbnCHTvb5FHHvNrdjPF"
