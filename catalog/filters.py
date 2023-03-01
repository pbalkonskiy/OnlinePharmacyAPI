from django_filters import rest_framework

from catalog.models import Product


class ProductFilter(rest_framework.FilterSet):
    """
    Custom filter to filter products from the catalog by a particular category or brand.
    Get query parameters in URL like '?category=<category>&brand=<brand>'.
    """
    brand = rest_framework.CharFilter(field_name="brand", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["category", "brand"]
