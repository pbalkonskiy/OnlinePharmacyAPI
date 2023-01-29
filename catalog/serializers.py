from rest_framework import serializers

from catalog.models import Product, Category, Manufacturer


class ProductSerializer(serializers.ModelSerializer):
    in_stock = serializers.BooleanField(source="in_stock", read_only=True)

    class Meta:
        model = Product
        # Not convince about this 'fields' attribute. Better test with views later.
        fields = ["__all__", "in_stock"]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["title", "parent_title"]


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"
