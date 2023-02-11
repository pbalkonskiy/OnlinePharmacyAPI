from django_filters import rest_framework

from catalog.models import Product


class ProductFilter(rest_framework.FilterSet):
    title = rest_framework.CharFilter(field_name="title", lookup_expr="icontains")
    brand = rest_framework.CharFilter(field_name="brand", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["category", "title", "brand"]
