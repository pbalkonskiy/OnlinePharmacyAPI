from rest_framework import serializers

from cart.serializers import PositionSerializer
from order.models import Order


class SimpleOrderSerializer(serializers.ModelSerializer):
    """
    Special serializer for the correct optimal display of the order list.
    """
    numb_of_positions = serializers.IntegerField(read_only=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "numb_of_positions", "total_price", "date", "payment_status"]


class OrderSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(read_only=True, many=True)
    expiration_date = serializers.DateTimeField(read_only=True)
    numb_of_positions = serializers.IntegerField(read_only=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer_id", "positions", "numb_of_positions", "total_price", "date",
                  "expiration_date", "delivery_method", "payment_method", "payment_status", "address",
                  "post_index"]
