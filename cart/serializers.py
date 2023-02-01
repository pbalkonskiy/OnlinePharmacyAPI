from rest_framework import serializers

from cart.models import Cart, Position
from catalog.models import Product


class SimpleProductSerializer(serializers.ModelSerializer):
    """
    Simplified version of product serializer specially to usage in position serializer
    with only few required in cart fields.
    """
    class Meta:
        model = Product
        fields = ["id", "title", "category", "price"]


class PositionSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    price = serializers.DecimalField(decimal_places=2, max_digits=10, read_only=False)

    class Meta:
        model = Position
        fields = ["id", "product", "cart", "amount", "price"]


class CartSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True)
    number_of_positions = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(decimal_places=2, max_digits=10, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "status", "positions", "number_of_positions", "total_price"]
