from rest_framework import serializers

from cart.serializers import PositionSerializer
from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(read_only=True, many=True)
    expiration_date = serializers.DateTimeField(read_only=True)
    numb_of_positions = serializers.IntegerField(read_only=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "positions", "numb_of_positions", "date", "expiration_date",
                  "delivery_method", "payment_method", "payment_status",
                  "address", "post_index", "total_price"]
