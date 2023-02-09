from rest_framework import serializers

from catalog.models import Product, Category, Manufacturer


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
        Overrode 'create' method specifically for the 'category' field with nested serializer.
        """
        category_data = validated_data.pop("category")
        category_instance = Category.objects.get(**category_data)
        product = Product.objects.create(category=category_instance, **validated_data)
        return product

    def update(self, instance, validated_data) -> Product:
        """
        Overrode 'create' method specifically for the 'category' field with nested serializer.
        """
        category_data = validated_data.pop("category")

        category = instance.category
        category.title = category_data.get("title", category.title)
        category.slug = category_data.get("slug", category.slug)
        category.parent_category = category_data.get("parent_category")
        category.save()

        instance.title = validated_data.get("title", instance.title)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.price = validated_data.get("price", instance.price)
        instance.brand = validated_data.get("brand", instance.brand)
        instance.manufacturer = validated_data.get("manufacturer", instance.manufacturer)
        instance.expiration_date = validated_data.get("expiration_date", instance.expiration_date)
        instance.barcode = validated_data.get("barcode", instance.barcode)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.info = validated_data.get("info", instance.info)
        instance.save()

        return instance


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
        # added 'in_stock' field in case the product in the cart position
        # is completely sold out to prevent it from getting into the order.


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"
