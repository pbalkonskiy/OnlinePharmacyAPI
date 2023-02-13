from rest_framework import serializers

from catalog.models import Product, Category, Manufacturer


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        exclude = ["id"]


class CategorySerializer(serializers.ModelSerializer):
    is_subcategory = serializers.BooleanField(read_only=True)
    parent_title = serializers.CharField(max_length=30, read_only=True)

    class Meta:
        model = Category
        fields = ["title", "slug", "is_subcategory", "parent_title"]
        lookup_field = "slug"  # purposely to add slug into the URL, have to add relevant attributes into views later.
        extra_kwargs = {
            "url": {
                "lookup_field": "slug"
            }
        }


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
    manufacturer = ManufacturerSerializer()
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ["title", "slug", "category", "price", "brand", "manufacturer", "expiration_date",
                  "addition_date", "barcode", "amount", "info", "is_in_stock"]
        lookup_field = "slug"
        extra_kwargs = {
            "url": {
                "lookup_field": "slug"
            }
        }

    def create(self, validated_data) -> Product:
        """
        Overriden 'create' method specifically for the 'category' & 'manufacturer'
        fields with nested serializer (POST).
        """
        category_data = validated_data.pop("category")
        category = Category.objects.get(**category_data)

        manufacturer_data = validated_data.pop("manufacturer")
        manufacturer = Manufacturer.objects.get(**manufacturer_data)

        return Product.objects.create(
            category=category,
            manufacturer=manufacturer,
            **validated_data,
        )

    def update(self, instance, validated_data) -> Product:
        """
        Overriden 'update' method specifically for the 'category' & 'manufacturer'
        fields with nested serializer (PUT & PATCH).
        """
        assert validated_data.get("category"), "Category nested serializer error."
        assert validated_data.get("manufacturer"), "Manufacturer nested serializer error."

        category_data, manufacturer_data = validated_data.get("category"), validated_data.get("manufacturer")

        category_serializer = CategorySerializer(data=category_data)
        manufacturer_serializer = ManufacturerSerializer(data=manufacturer_data)

        if category_serializer.is_valid() and manufacturer_serializer.is_valid():
            category = category_serializer.update(
                instance=instance.category,
                validated_data=category_serializer.validated_data
            )
            manufacturer = manufacturer_serializer.update(
                instance=instance.manufacturer,
                validated_data=manufacturer_serializer.validated_data
            )
            validated_data["category"], validated_data["manufacturer"] = category, manufacturer

        return super().update(instance, validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    """
    Simplified version of product serializer specially to use in position serializer
    with only few required fields.
    """
    price = serializers.FloatField()
    category = SimpleCategorySerializer(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    url = serializers.URLField(read_only=True)

    class Meta:
        model = Product
        fields = ["url", "title", "category", "brand", "price", "is_in_stock"]
        # added 'is_in_stock' field in case the product in the cart position
        # is completely sold out to prevent it from getting into the order.
