import pytest
from django.contrib.auth import get_user_model
from users.models import UserLogin
from users.signals.user_login_signal import web3_login_done

