from rest_framework import viewsets
from rest_framework import status
from core.mixins import ResponseMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from .models import Cart, CartItem

class CartViewSet(viewsets.ViewSet, ResponseMixin):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def add_cart_item(self, request):
        pass

