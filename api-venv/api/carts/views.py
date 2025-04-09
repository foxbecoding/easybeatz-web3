from rest_framework import viewsets
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from core.mixins import ResponseMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from .models import Cart, CartItem
from albums.enums import TrackPriceEnum
from albums.models import TrackPrice, TrackExclusivePrice

class CartViewSet(viewsets.ViewSet, ResponseMixin):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def add_cart_item(self, request):
        cart_id = getattr(request, "cart_id", None)
        if not cart_id:
            return self.view_response("Cart ID not found", None, status.HTTP_400_BAD_REQUEST)

        pricing_type = request.data.get("type")
    
        valid_types = [
            TrackPriceEnum.TRACK_PRICE.value,
            TrackPriceEnum.TRACK_EXCLUSIVE_PRICE.value
        ]

        if pricing_type not in valid_types:
            return self.view_response("Invalid track pricing", None, status.HTTP_400_BAD_REQUEST)

        content_type = None
        
        if pricing_type == TrackPriceEnum.TRACK_PRICE.value:
            content_type = ContentType.objects.get_for_model(TrackPrice)
        else:
            content_type = ContentType.objects.get_for_model(TrackExclusivePrice)

        return self.view_response("", None, status.HTTP_200_OK)
