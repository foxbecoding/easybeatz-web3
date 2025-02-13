from django.dispatch import receiver, Signal
from ..models import User, UserLogin

web3_login_done = Signal()

@receiver(web3_login_done)
def web3_login_done_handler(sender, user: User, **kwargs): 
    user_login = UserLogin(user = user)
    user_login.save()
