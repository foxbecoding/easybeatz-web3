from rest_framework import serializers
from ..models import Cart, CartItem
from albums.enums import TrackPriceEnum

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
        if obj.price_type == TrackPriceEnum.TRACK_PRICE.value:
            return obj.track.price.value if obj.track.price else None
        elif obj.price_type == TrackPriceEnum.TRACK_EXCLUSIVE_PRICE.value:
            return obj.track.exclusive_price.value if obj.track.exclusive_price else None
        return None

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
    # items = ItemsField(read_only=True, many=True) 
    class Meta:
        model = Cart
        fields = ["items"]


    # items = serializers.SerializerMethodField()
   
    # def get_items(self, obj):
    #     items = obj.items.all()
    #     collection = []
    #     for item in items:
    #         price_map = {
    #             TrackPriceEnum.TRACK_PRICE.value: item.track.price.value,
    #             TrackPriceEnum.TRACK_EXCLUSIVE_PRICE.value: .track.exclusive_price.value,
    #         }
    #        collection.append() 
    #     return collection

