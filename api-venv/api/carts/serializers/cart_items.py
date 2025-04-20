from rest_framework import serializers
from ..models import CartItem

class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ['cart', 'track', 'price_model_type', 'price_model_id']

    def to_representation(self, instance):
        # Add price model representation for serialization
        rep = super().to_representation(instance)
        rep['price_model'] = str(instance.price_model)  # You can modify this as needed
        return rep
