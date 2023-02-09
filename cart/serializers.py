from rest_framework import serializers

from cart.models import Cart, Position

from catalog.serializers import SimpleProductSerializer


class PositionSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    price = serializers.DecimalField(decimal_places=2, max_digits=10, read_only=False)

    class Meta:
        model = Position
        fields = ["product", "amount", "price"]


class CartSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True)
    numb_of_positions = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(decimal_places=2, max_digits=10, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "status", "positions", "numb_of_positions", "total_price"]
