from django.db import models
from django.db.models import Prefetch, Q, Count
from django.apps import apps

class CartManager(models.Manager):
    def get_cart_items(self, cart_id: str, user):
       
        CartItem = apps.get_model('carts', 'CartItem')
        
        user_type = str(user)

        cart_filter = Q(cart_id=cart_id, user=user, deleted__isnull=True) if user_type != "AnonymousUser" else Q(cart_id=cart_id, user__isnull=True, deleted__isnull=True)

        queryset = self.select_related("user").prefetch_related(
            Prefetch(
                "items",
                queryset=CartItem.objects.select_related(
                    "track",
                    "track__display",
                    "track__album", 
                    "track__album__station",
                    "track__album__station__user",
                    "track__album__station__picture", 
                    "track__album__cover",
                    "track__exclusive_price",
                    "track__price",
                ).only(
                    "price_model_type", "price_model_id", 
                    "track__title", "track__tid", "track__duration", "track__order_no",
                    "track__album__aid",
                    "track__album__cover__picture",
                    "track__display__audio",
                    "track__exclusive_price__value",
                    "track__price__value",
                    "track__album__station__handle", "track__album__station__name",
                    "track__album__station__picture__picture",
                    "track__album__station__user__pubkey"
                ).filter(track__is_exclusive_sold=False, deleted__isnull=True)
            )
        ).annotate(
            item_count=Count("items")
        ).filter(cart_filter).first()


        return queryset
