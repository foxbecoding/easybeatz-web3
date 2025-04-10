from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import CartItem
from albums.models import Track, TrackPrice, TrackExclusivePrice

class CartItemSerializer(serializers.ModelSerializer):
    # Price model will be determined by the backend (ContentType-based)
    # price_model_id = serializers.IntegerField()
    # price_model_type = serializers.CharField()

    class Meta:
        model = CartItem
        fields = ['cart', 'track', 'price_model_type', 'price_model_id']

    def create(self, validated_data):
        # Extract price model type and get the actual content type
        price_model_type = validated_data.pop('price_model_type')
        price_model_id = validated_data.pop('price_model_id')

        # Get the actual price model instance (e.g., TrackPrice, TrackExclusivePrice)
        price_model_instance = price_model_type.get_object_for_this_type(id=price_model_id)

        # Create CartItem with the price model
        return CartItem.objects.create(
            cart=validated_data['cart'],
            track=validated_data['track'],
            price_model_type=price_model_type,
            price_model_id=price_model_id,
            price_model=price_model_instance,
        )

    def to_representation(self, instance):
        # Add price model representation for serialization
        rep = super().to_representation(instance)
        rep['price_model'] = str(instance.price_model)  # You can modify this as needed
        return rep
