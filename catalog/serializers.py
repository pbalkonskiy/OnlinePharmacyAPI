from rest_framework import serializers

from catalog.models import Product, Category, Manufacturer


class CategorySerializer(serializers.ModelSerializer):
    is_subcategory = serializers.BooleanField(read_only=True)
    parent_title = serializers.CharField(max_length=30, read_only=True)

    class Meta:
        model = Category
        fields = ["title", "slug", "is_subcategory", "parent_title"]


class SimpleCategorySerializer(serializers.ModelSerializer):
    """
    Simplified version of category serializer.
    """
    class Meta:
        model = Category
        fields = ["title"]


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()
    category = CategorySerializer()
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ["title", "slug", "category", "price", "brand", "manufacturer", "expiration_date",
                  "addition_date", "barcode", "amount", "info", "is_in_stock"]


class SimpleProductSerializer(serializers.ModelSerializer):
    """
    Simplified version of product serializer specially to use in position serializer
    with only few required fields.
    """
    price = serializers.FloatField()
    category = SimpleCategorySerializer()
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ["title", "category", "brand", "price", "is_in_stock"]
        # added 'in_stock' field in case the product in the cart position
        # is completely sold out to prevent it from getting into the order.


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"
