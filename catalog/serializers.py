from rest_framework import serializers

from catalog.models import Product, Category, Manufacturer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["title", "parent_title"]


class ProductSerializer(serializers.ModelSerializer):
    is_in_stock = serializers.BooleanField(read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ["id", "category", "price", "brand", "manufacturer", "expiration_date",
                  "addition_date", "barcode", "amount", "info", "is_in_stock"]


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"
