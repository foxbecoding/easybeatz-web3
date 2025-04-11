from rest_framework import viewsets
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from core.mixins import ResponseMixin
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .models import Cart
from .serializers import CartItemSerializer
from .services.cart_service import add_item_to_cart
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

        tid = request.data.get("tid")
        pricing_type = request.data.get("type")

        success, message, data = add_item_to_cart(cart_id, tid, pricing_type, request.user)

        if not success:
            return self.view_response(message, data, status.HTTP_400_BAD_REQUEST)

        return self.view_response(message, data, status.HTTP_201_CREATED)
