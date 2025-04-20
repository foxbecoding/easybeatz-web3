from django.dispatch import receiver, Signal
from django.utils.timezone import now
from django.db import transaction
from ..models import User, UserLogin
from carts.models import Cart, CartItem

web3_login_done = Signal()

@receiver(web3_login_done)
@transaction.atomic
def web3_login_done_handler(sender, user: User, request=None, **kwargs): 
    user_login = UserLogin(user = user)
    user_login.save()
    _sync_cart(user, request)


def _sync_cart(user:User, request=None):
    if request is None:
        return  # Can't sync cart without request

    cookie_cart_id = request.COOKIES.get('cart_id')
    if not cookie_cart_id:
        return

    try:
        cookie_cart = Cart.objects.prefetch_related('items').get(
            cart_id=cookie_cart_id,
            user__isnull=True,
            deleted__isnull=True
        )
    except Cart.DoesNotExist:
        return

    # Get or create user's cart
    user_cart, created = Cart.objects.get_or_create(user=user, deleted__isnull=True)

    # If it's the same cart already
    if user_cart.cart_id == cookie_cart.cart_id:
        return

    for item in cookie_cart.items.all():
        exists = CartItem.objects.filter(
            cart=user_cart,
            track=item.track,
            price_model_type=item.price_model_type,
            price_model_id=item.price_model_id,
        ).exists()
        if not exists:
            item.pk = None  # clone item
            item.cart = user_cart
            item.save()

    cookie_cart.deleted = now()
    cookie_cart.save()

    # Optionally update the request object for further use
    request.cart_id = user_cart.cart_id
