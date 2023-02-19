from rest_framework import serializers

from cart.models import Cart, Position

from catalog.models import Product
from catalog.serializers import SimpleProductSerializer


class PositionSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    slug = serializers.SlugRelatedField(read_only=True, source="product", slug_field="slug")
    price = serializers.FloatField(read_only=False)

    class Meta:
        model = Position
        fields = ["id", "slug", "cart", "product", "price", "amount"]


class AddPositionSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        cart_id = self.context["user_id"]
        product_id = self.validated_data["product_id"]
        amount = self.validated_data["amount"]

        try:
            cart_item = Position.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.amount = amount
            cart_item.save()
            self.instance = cart_item
        except Position.DoesNotExist:
            self.instance = Position.objects.create(cart_id=cart_id, product_id=product_id, amount=amount)

        return self.instance

    def validate_product_id(self, value):
        """
        If the product with passed ID exists in catalog.
        """
        try:
            assert Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")
        return value

    def validate_amount(self, value):
        """
        If the passed 'amount' value does not exceed product's 'amount' field.
        """
        product_id = self.initial_data.get("product_id")
        try:
            product = Product.in_stock.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product is not in stock.")
        if value > product.amount:
            raise serializers.ValidationError("Amount cannot exceed the available stock.")
        return value

    class Meta:
        model = Position
        fields = ["product_id", "amount", "price"]


class UpdatePositionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(min_value=1)

    def validate_id(self, value):
        """
        Checks if the position exists in the cart and get the related product.
        """
        try:
            position = Position.objects.get(id=value)
        except Position.DoesNotExist:
            raise serializers.ValidationError("Position does not exist in the cart.")

        product = position.product
        self.context["product"] = product  # Save the related product for later use

        return value

    def validate_amount(self, value):
        """
        Checks if the passed in PATCH request method 'amount' value not exceed the 'amount'
        field value of the related product from the 'Product' table.
        """
        product = self.context.get("product")
        if product is not None and value > product.amount:
            raise serializers.ValidationError("Amount cannot exceed the available stock.")
        return value

    def save(self, **kwargs):
        self.is_valid(raise_exception=True)
        cart_id = self.context["user_id"]
        amount = self.validated_data["amount"]
        position_id = self.validated_data["id"]
        try:
            cart_item = Position.objects.get(id=position_id, cart_id=cart_id)
            cart_item.amount = amount
            cart_item.save()
            self.instance = cart_item
        except Position.DoesNotExist:
            self.instance = Position.objects.create(id=position_id, cart_id=cart_id, amount=amount)
        return self.instance

    class Meta:
        model = Position
        fields = ["id", "amount"]


class CartSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True)
    numb_of_positions = serializers.IntegerField(read_only=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "positions", "numb_of_positions", "total_price"]
