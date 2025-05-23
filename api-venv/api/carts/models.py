from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .managers import CartManager
from users.models import User
from albums.models import Track, TrackPrice, TrackExclusivePrice
from albums.enums import TrackPriceEnum
import uuid

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    cart_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    objects = models.Manager()
    carts = CartManager()
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    track = models.ForeignKey(Track, related_name="cart_items", on_delete=models.CASCADE)
    price_model_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    price_model_id = models.PositiveIntegerField()
    price_model = GenericForeignKey('price_model_type', 'price_model_id')
    objects = models.Manager()
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'track', 'price_model_type'],
                name='unique_cart_item'
            )
        ]

    @property
    def price_type(self):
        value = None
        if ContentType.objects.get_for_model(TrackPrice) == self.price_model_type:
            value = TrackPriceEnum.TRACK_PRICE.value
        elif ContentType.objects.get_for_model(TrackExclusivePrice) == self.price_model_type: 
            value = TrackPriceEnum.TRACK_EXCLUSIVE_PRICE.value
        return value
