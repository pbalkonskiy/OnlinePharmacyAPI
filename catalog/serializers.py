from rest_framework import serializers

from catalog.models import Product, Category, Manufacturer


class ProductSerializer(serializers.ModelSerializer):
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "category", "price", "brand", "manufacturer", "expiration_date",
                  "addition_date", "barcode", "amount", "info", "in_stock"]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["title", "parent_title"]


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"
