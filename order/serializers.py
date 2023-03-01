from rest_framework import serializers

from cart.serializers import PositionSerializer

from order.models import Order

from catalog.models import Pharmacy
from catalog.serializers import PharmacySerializer


class SimpleOrderSerializer(serializers.ModelSerializer):
    """
    Special serializer for the correct optimal display of the order list.
    """
    key = serializers.IntegerField(read_only=True)
    url = serializers.URLField(read_only=True)
    customer_id = serializers.IntegerField(read_only=True)
    numb_of_positions = serializers.IntegerField(read_only=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "url", "key", "customer_id", "numb_of_positions",
                  "total_price", "created_at", "delivery_method", "payment_status",
                  "is_paid", "in_progress", "closed"]


class OrderAddSerializer(serializers.ModelSerializer):
    """
    Special serializer for cart application to create a new order based on the cart
    positions list reviewed using POST method.
    """
    customer_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer_id"]


class OrderSerializer(serializers.ModelSerializer):
    key = serializers.IntegerField(read_only=True)
    customer_id = serializers.IntegerField(read_only=True)
    positions = PositionSerializer(read_only=True, many=True)
    numb_of_positions = serializers.IntegerField(read_only=True)
    total_price = serializers.FloatField(read_only=True)
    pharmacy = PharmacySerializer(many=False)

    class Meta:
        model = Order
        fields = ["id", "key", "customer_id", "positions", "numb_of_positions",
                  "total_price", "created_at", "delivery_method", "payment_method",
                  "payment_status", "is_paid", "address", "post_index", "pharmacy",
                  "receipt_date", "receipt_time"]
        lookup_field = "id"
        extra_kwargs = {
            "url": {
                "lookup_field": "id"
            }
        }


class OrderCheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["delivery_method", "payment_method", "address", "post_index"]

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        order_id = instance.id

        delivery_method = self.validated_data["delivery_method"]
        payment_method = self.validated_data["payment_method"]
        address = self.validated_data["address"]
        post_index = self.validated_data["post_index"]

        order_item = Order.objects.get(id=order_id)
        order_item.delivery_method = delivery_method
        order_item.payment_method = payment_method
        order_item.address = address
        order_item.post_index = post_index

        if order_item.delivery_method == "Door delivery" and order_item.payment_method == "Prepayment":
            order_item.payment_status = "Pending payment"
        else:
            order_item.payment_status = "Payment upon receipt"

        order_item.save()
        self.instance = order_item
        return self.instance

    def validate(self, attrs):
        """
        Validates order parameters compatability and post index value.
        """
        delivery_method = attrs.get("delivery_method")
        payment_method = attrs.get("payment_method")
        address = attrs.get("address")
        index = attrs.get("post_index")

        if delivery_method and payment_method:
            if delivery_method == "Door delivery" and payment_method == "Prepayment":
                pass
            elif delivery_method == "Self-delivery" and payment_method == "Upon receipt":
                if address or index:
                    raise serializers.ValidationError(
                        "You don't need to enter the address or post index if you use self-delivery."
                    )
            else:
                raise serializers.ValidationError(
                    "Sorry, you can't use this payment method with the delivery method here."
                )

        if index and len(str(index)) > 6:
            raise serializers.ValidationError("Post index should not be longer than 6 symbols.")

        return attrs


class OrderBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["pharmacy", "receipt_date", "receipt_time"]

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        order_id = instance.id

        pharmacy = self.validated_data["pharmacy"]
        receipt_date = self.validated_data["receipt_date"]
        receipt_time = self.validated_data["receipt_time"]

        order_item = Order.objects.get(id=order_id)
        order_item.pharmacy = pharmacy
        order_item.receipt_date = receipt_date
        order_item.receipt_time = receipt_time

        order_item.save()
        self.instance = order_item
        return self.instance

    def validate(self, attrs):
        """
        Validates serializer fields and if the pickup time does not coincide with the
        working hours of the pharmacy.
        """
        pharmacy = attrs.get("pharmacy")
        receipt_time = attrs.get("receipt_time")

        try:
            pharmacy = Pharmacy.objects.get(id=pharmacy.id)
            if not pharmacy.opened_at <= receipt_time <= pharmacy.closed_at:
                serializers.ValidationError("Invalid self-delivery time.")
        except Pharmacy.DoesNotExist:
            serializers.ValidationError("There is no pharmacy with such ID in the list.")

        return attrs
