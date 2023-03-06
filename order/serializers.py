from datetime import datetime, timedelta

from rest_framework import serializers

from catalog.models import Pharmacy
from catalog.serializers import PharmacySerializer

from cart.serializers import PositionSerializer
from cart.models import Position

from order.models import Order
from order.constants import DELIVERY_STATUS

from users.serializers import CustomerForManagerSerializer


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
        fields = ["id", "url", "key", "customer_id", "numb_of_positions", "total_price", "created_at",
                  "delivery_method", "delivery_status", "payment_status", "is_paid", "in_progress", "closed"]


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
        fields = ["id", "key", "customer_id", "positions", "numb_of_positions", "total_price", "created_at",
                  "delivery_method", "delivery_status", "payment_method", "payment_status", "is_paid",
                  "address", "post_index", "pharmacy", "receipt_date", "receipt_time"]
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
        Validates serializer fields and checks if the pickup time does not coincide with the
        working hours of the pharmacy.

        Also, there is a check whether the order date is overdue or the time parameter is invalid
        (self-delivery order can be picked up not earlier than 2 hours after registration).
        """

        instance = self.instance  # current order
        pharmacy = attrs.get("pharmacy")
        receipt_time = attrs.get("receipt_time")
        receipt_date = attrs.get("receipt_date")

        if instance and receipt_date and receipt_time:

            required = datetime.now() + timedelta(hours=2)
            if datetime.combine(receipt_date, receipt_time) < required:
                raise serializers.ValidationError("Invalid receipt date or time parameter.")

        else:
            raise serializers.ValidationError("Additional information (receipt date or time) required.")

        if pharmacy:
            pharmacy = Pharmacy.objects.get(id=pharmacy.id)
            if not pharmacy.opened_at <= receipt_time <= pharmacy.closed_at:
                raise serializers.ValidationError("Invalid self-delivery time.")
        else:
            raise serializers.ValidationError("Additional information (pharmacy) required.")

        return attrs


class DeliveryManConfirmSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(read_only=True, many=True)
    customer = CustomerForManagerSerializer(read_only=True)

    new_delivery_status = serializers.CharField(write_only=True)
    address = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'positions', 'delivery_method', 'delivery_status', 'is_paid',
                  'in_progress', 'address', 'post_index', 'new_delivery_status', 'closed']
        read_only_fields = ['customer', 'positions', 'delivery_method', 'delivery_status',
                            'is_paid', 'in_progress', 'address', 'post_index', ]
        lookup_field = "id"

    def update(self, instance: Order, validated_data):
        if instance.is_paid and not instance.closed and instance.in_progress:
            print(validated_data.get("new_delivery_status"))
            instance.delivery_status = validated_data.get("new_delivery_status")

            if instance.delivery_status == 'Delivered':
                instance.closed = True
                instance.in_progress = False
            instance.save()
            return instance
        else:
            serializers.ValidationError('Something wrong with orders status')

    def validate_new_delivery_status(self, value):
        choices = dict(DELIVERY_STATUS)
        if value not in choices.values():
            print(choices.values())
            raise serializers.ValidationError(f"{value} is not a valid choice for delivery status.")
        return value


class ManagerSellerOrderSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(read_only=True, many=True)
    customer = CustomerForManagerSerializer(read_only=True)
    pharmacy = PharmacySerializer(read_only=True)
    key = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'key', 'delivery_method', "receipt_date", "receipt_time", "closed",
                  'pharmacy', 'customer', 'positions']

    def update(self, instance: Order, validated_data):
        instance.in_progress = False
        instance.closed = True
        instance.is_paid = True

        positions = Position.objects.filter(order=instance)
        for position in positions:
            product = position.product
            product.amount -= position.amount
            product.save()

        instance.save()
        return instance

