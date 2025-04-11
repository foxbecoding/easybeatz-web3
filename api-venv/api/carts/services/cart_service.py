from django.contrib.contenttypes.models import ContentType
from ..models import Cart, Track
from ..serializers import CartItemSerializer
from albums.enums import TrackPriceEnum
from albums.models import TrackPrice, TrackExclusivePrice


def add_item_to_cart(cart_id: str, tid: str, pricing_type: str, user=None):
    valid_type_model_map = {
        TrackPriceEnum.TRACK_PRICE.value: TrackPrice,
        TrackPriceEnum.TRACK_EXCLUSIVE_PRICE.value: TrackExclusivePrice,
    }

    if pricing_type not in valid_type_model_map:
        return False, "Invalid track pricing", None

     # Determine the appropriate cart based on auth state
    if user and user.is_authenticated:
        cart_instance, created = Cart.objects.get_or_create(
            user=user,
            deleted__isnull=True,
            defaults={"cart_id": cart_id}  # only used if new cart is created
        )
    else:
        cart_instance, created = Cart.objects.get_or_create(
            cart_id=cart_id,
            user__isnull=True,
            deleted__isnull=True
        )

    track_instance = Track.objects.filter(tid=tid).first()
    if not track_instance:
        return False, "Track not found", None

    price_model_ct = ContentType.objects.get_for_model(valid_type_model_map[pricing_type])

    data = {
        'cart': cart_instance.pk,
        'track': track_instance.pk,
        'price_model_type': price_model_ct.pk,
        'price_model_id': track_instance.pk
    }

    serializer = CartItemSerializer(data=data)
    if not serializer.is_valid():
        return False, "Validation error", serializer.errors

    serializer.save()
    return True, "Added to cart", { "tid": tid, "type": pricing_type }
