import pytest
from django.contrib.auth import get_user_model
from users.models import UserLogin
from users.signals.user_login_signal import web3_login_done

@pytest.mark.django_db
def test_web3_login_done_handler(default_user):
    """Test that the web3_login_done signal creates a UserLogin record."""

    # Ensure no UserLogin records exist before the signal
    assert UserLogin.objects.filter(user=default_user).count() == 0

    # Send the web3_login_done signal
    web3_login_done.send(sender=None, user=default_user)

    # Verify that a UserLogin record is created
    assert UserLogin.objects.filter(user=default_user).count() == 1
