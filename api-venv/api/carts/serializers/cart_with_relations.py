from rest_framework import serializers
from ..models import Cart, CartItem
from albums.enums import TrackPriceEnum

class ItemsField(serializers.RelatedField):
    def to_representation(self, value):
        price_map = {
            TrackPriceEnum.TRACK_PRICE.value: value.track.price.value,
            TrackPriceEnum.TRACK_EXCLUSIVE_PRICE.value: value.track.exclusive_price.value,
        }
        return {
            "type": value.price_type,
            "track": {
                "tid": value.track.tid,
                "title": value.track.title,
                "duration": value.track.duration,
                "formatted_duration": value.track.formatted_duration,
                "display": value.track.display.display_url,
                "order_no": value.track.order_no,
                "price": price_map.get(value.price_type)
            },
            "album": {
                "aid": value.track.album.aid,
                "cover": value.track.album.cover.cover_url,
            },
            "station": {
                "name": value.track.album.station.name,
                "handle": value.track.album.station.handle,
                "picture": value.track.album.station.picture_url,
                "pubkey": value.track.album.station.user.pubkey
            }
        }

class CartWithRelationsSerializer(serializers.ModelSerializer):
    items = ItemsField(read_only=True) 

    class Meta:
        model = Cart
        fields = ["items"]

