from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from ..models import Cart, CartItem
from ..serializers import CartWithRelationsSerializer, CartItemSerializer
from albums.enums import TrackPriceEnum
from albums.models import Track, TrackPrice, TrackExclusivePrice

def get_cart_items(cart_id: str, user):
    cart_items = Cart.carts.get_cart_items(cart_id, user)

    if not cart_items:
        return None

    serializer = CartWithRelationsSerializer(cart_items)
    return serializer.data

def add_item_to_cart(cart_id: str, tid: str, pricing_type: str, user=None):
    # Step 1: Map pricing types to their models
    track_model = _get_track_model(pricing_type)
    if not track_model:
        return False, "Invalid track pricing type", None

    # Step 2: Fetch or create the cart
    cart_instance = _get_or_create_cart(cart_id, user)

    # Step 3: Get the track
    track_instance = Track.objects.filter(tid=tid).first()
    if not track_instance:
        return False, "Track not found", None

    # Step 4: Get the content type of the pricing model
    try:
        price_model_ct = ContentType.objects.get_for_model(track_model)
    except ContentType.DoesNotExist:
        return False, "Content type not found", None

    # Step 5: Prepare serializer data
    data = {
        'cart': cart_instance.pk,
        'track': track_instance.pk,
        'price_model_type': price_model_ct.pk,
        'price_model_id': track_instance.pk,  # Note: might want to confirm if this is correct
    }

    serializer = CartItemSerializer(data=data)
    if not serializer.is_valid():
        return False, "Validation error", serializer.errors

    serializer.save()
    cart_items = get_cart_items(cart_id, user)

    return True, "Track added to cart", cart_items

def remove_cart_item(cart_id: str, tid: str, pricing_type: str, user=None):
    track_model = _get_track_model(pricing_type)

    if not track_model:
        return False, "Invalid track pricing type", None

    try:
        price_model_ct = ContentType.objects.get_for_model(track_model)
    except ContentType.DoesNotExist:
        return False, "Content type not found", None

    cart_item_instance = CartItem.objects.filter(
        cart__cart_id=cart_id,
        track__tid=tid,
        price_model_type=price_model_ct.pk,
        deleted__isnull=True
    ).first()

    if not cart_item_instance:
        return False, "Invalid cart item", None

    cart_item_instance.deleted = now()
    cart_item_instance.save()

    cart_items = get_cart_items(cart_id, user)

    return True, "Track removed from cart", cart_items

def _get_track_model(pricing_type: str):
    valid_type_model_map = {
        TrackPriceEnum.TRACK_PRICE.value: TrackPrice,
        TrackPriceEnum.TRACK_EXCLUSIVE_PRICE.value: TrackExclusivePrice,
    }

    return valid_type_model_map.get(pricing_type)

def _get_or_create_cart(cart_id, user):
    if user and user.is_authenticated:
        cart_instance, _ = Cart.objects.get_or_create(
            user=user,
            deleted__isnull=True,
            defaults={"cart_id": cart_id}
        )
    else:
        cart_instance, _ = Cart.objects.get_or_create(
            cart_id=cart_id,
            user__isnull=True,
            deleted__isnull=True
        )
    return cart_instance
