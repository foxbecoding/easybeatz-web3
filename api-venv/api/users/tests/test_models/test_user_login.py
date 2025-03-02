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


