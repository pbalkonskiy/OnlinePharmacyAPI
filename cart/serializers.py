from rest_framework import serializers

from cart.models import Cart, Position

from catalog.serializers import SimpleProductSerializer


class PositionSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    price = serializers.FloatField(read_only=False)

    class Meta:
        model = Position
        fields = ["id", "cart", "product", "price", "amount"]


class AddPositionSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        amount = self.validated_data["amount"]

        try:
            cart_item = Position.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.amount = amount
            cart_item.save()
            self.instance = cart_item
        except:
            self.instance = Position.objects.create(cart_id=cart_id, product_id=product_id, amount=amount)

        return self.instance

    class Meta:
        model = Position
        fields = ["product_id", "amount", "price"]


class CartSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True)
    numb_of_positions = serializers.IntegerField(read_only=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "positions", "numb_of_positions", "total_price"]
