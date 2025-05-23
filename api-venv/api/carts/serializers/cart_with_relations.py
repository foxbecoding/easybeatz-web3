from rest_framework import serializers
from ..models import Cart, CartItem
from albums.enums import TrackPriceEnum

def track_price_setter(track, price_type: str):
    price_map = {
        TrackPriceEnum.TRACK_PRICE.value: getattr(track.price, 'value', None),
        TrackPriceEnum.TRACK_EXCLUSIVE_PRICE.value: getattr(getattr(track, 'exclusive_price', None), 'value', None),
    }
    return price_map.get(price_type)

class CartItemWithRelationsSerializer(serializers.ModelSerializer):
    price_type = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    track = serializers.SerializerMethodField()
    album = serializers.SerializerMethodField()
    station = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["price_type", "price", "track", "album", "station"]

    def get_price_type(self, obj):
        return obj.price_type

    def get_price(self, obj):
        return track_price_setter(obj.track, obj.price_type)

    def get_track(self, obj):
        track = obj.track
        return {
            "tid": track.tid,
            "title": track.title,
            "duration": track.duration,
            "formatted_duration": track.formatted_duration,
            "display": track.display.display_url,
            "order_no": track.order_no,
        }

    def get_album(self, obj):
        album = obj.track.album
        return {
            "aid": album.aid,
            "cover": album.cover.cover_url if album.cover else None
        }

    def get_station(self, obj):
        station = obj.track.album.station
        return {
            "name": station.name,
            "handle": station.handle,
            "picture": station.picture.picture.url if station.picture else None,
            "pubkey": station.user.pubkey
        }

class CartWithRelationsSerializer(serializers.ModelSerializer):
    items = CartItemWithRelationsSerializer(many=True, read_only=True)
    cart_count = serializers.SerializerMethodField()
    cart_subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "items",
            "cart_count",
            "cart_subtotal"
        ]

    def get_cart_count(self, obj):
        return obj.items.count()

    def get_cart_subtotal(self, obj):
        prices = []
        for item in obj.items.all():
            track = item.track
            price = track_price_setter(track, item.price_type)
            prices.append(price)
        return sum(prices)
