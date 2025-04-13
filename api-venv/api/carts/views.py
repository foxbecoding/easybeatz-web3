from rest_framework import viewsets
from rest_framework import status
from core.mixins import ResponseMixin
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .services.cart_service import add_item_to_cart, get_cart_items

class CartViewSet(viewsets.ViewSet, ResponseMixin):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def get_cart(self, request):
        cart_id = getattr(request, "cart_id", None)
        if not cart_id:
            return self.view_response("Cart ID not found", None, status.HTTP_400_BAD_REQUEST)

        data = get_cart_items(cart_id, request.user)

        return self.view_response(None, data, status.HTTP_200_OK)

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
