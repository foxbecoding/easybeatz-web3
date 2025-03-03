import pytest
from users.models import UserLogin
from users.tests.factories import UserFactory, UserLoginFactory

@pytest.mark.django_db
def test_create_user_login():
    """
    Ensure a UserLogin model can be created successfully.
    """
    user = UserFactory()
    user_login = UserLogin.objects.create(user=user)
    assert user_login.pk is not None  # Check if saved to the DB
    assert user_login.user == user  # Ensure ForeignKey relationship is set


@pytest.mark.django_db
def test_user_login_factory_creates_valid_user_login():
    """
    Ensure that the UserLoginFactory correctly creates a UserLogin instance.
    """
    user_login = UserLoginFactory()
    assert user_login.pk is not None
    assert user_login.user is not None  # Ensure ForeignKey is assigned


@pytest.mark.django_db
def test_user_login_default_fixture(default_user_login):
    """
    Ensure that the default_user_login fixture creates a valid UserLogin instance.
    """
    assert default_user_login.pk is not None  # Check if saved to the DB
    assert isinstance(default_user_login, UserLogin)  # Ensure it's a UserLogin instance
    assert default_user_login.user is not None 
