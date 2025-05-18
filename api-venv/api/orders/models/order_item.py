from django.db import models
from orders.models import Order
from stations.models import Station
from albums.models import Track

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='track_orders'
    )
    track = models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.pk)
