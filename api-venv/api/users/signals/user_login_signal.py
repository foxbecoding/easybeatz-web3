from django.dispatch import receiver, Signal
from ..models import User, UserLogin

web3_login_done = Signal()

