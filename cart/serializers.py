from rest_framework import serializers

from cart.models import Cart, Position

from catalog.serializers import SimpleProductSerializer


class PositionSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    price = serializers.FloatField(read_only=False)

    class Meta:
        model = Position
        fields = ["id", "cart", "product", "price", "amount"]


class CartSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True)
    numb_of_positions = serializers.IntegerField(read_only=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "positions", "numb_of_positions", "total_price"]
