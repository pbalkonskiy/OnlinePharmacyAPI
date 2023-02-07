from rest_framework import serializers

from cart.models import Cart, Position

from catalog.models import Product
from catalog.serializers import CategorySerializer


class SimpleProductSerializer(serializers.ModelSerializer):
    """
    Simplified version of product serializer specially to usage in position serializer
    with only few required in cart fields.
    """
    is_in_stock = serializers.BooleanField(read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ["id", "title", "category", "price", "is_in_stock"]
        # added 'in_stock' field in case the product in the cart position
        # is completely sold out to prevent it from getting into the order.


class PositionSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    price = serializers.DecimalField(decimal_places=2, max_digits=10, read_only=False)

    class Meta:
        model = Position
        fields = ["id", "product", "cart", "amount", "price"]


class CartSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True)
    numb_of_positions = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(decimal_places=2, max_digits=10, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "status", "positions", "numb_of_positions", "total_price"]
