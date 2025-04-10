from rest_framework import viewsets
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from core.mixins import ResponseMixin
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .models import Cart
from .serializers import CartItemSerializer
from albums.enums import TrackPriceEnum
from albums.models import Track, TrackPrice, TrackExclusivePrice

class CartViewSet(viewsets.ViewSet, ResponseMixin):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def add_cart_item(self, request):
        cart_id = getattr(request, "cart_id", None)
        if not cart_id:
            return self.view_response("Cart ID not found", None, status.HTTP_400_BAD_REQUEST)

        valid_type_model_map = {
            TrackPriceEnum.TRACK_PRICE.value: TrackPrice,
            TrackPriceEnum.TRACK_EXCLUSIVE_PRICE.value: TrackExclusivePrice,
        }

        pricing_type = request.data.get("type")

        if pricing_type not in valid_type_model_map:
            return self.view_response("Invalid track pricing", None, status.HTTP_400_BAD_REQUEST)

        track_price_ct = ContentType.objects.get_for_model(valid_type_model_map[pricing_type])

        tid = request.data.get("tid")
        if not tid:
            return self.view_response("Invalid Track ID", None, status.HTTP_400_BAD_REQUEST)

        cart_instance = Cart.objects.get(cart_id=cart_id)
        track_instance = Track.objects.filter(tid=tid).first()
        if not track_instance:
            return self.view_response("Track not found", None, status.HTTP_400_BAD_REQUEST)

        data = {
            'cart': cart_instance,
            'track': track_instance,
            'price_model_type': track_price_ct,
            'price_model_id': track_instance.pk
        }

        serializer = CartItemSerializer(data=data)
        if not serializer.is_valid():
            return self.view_response("Error adding cart item", serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save(cart=cart_instance, track=track_instance)
        return self.view_response("Added to cart", { "tid": tid, "type": pricing_type }, status.HTTP_201_CREATED)
