from rest_framework import mixins
from rest_framework import viewsets

from catalog.models import Product
from catalog.serializers import (SimpleProductSerializer,
                                 ProductSerializer)
from catalog.paginations import CatalogListPagination


class CatalogListViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """
    ViewSet for browsing the catalog as a list of products.
    """
    queryset = Product.objects.all()
    serializer_class = SimpleProductSerializer
    pagination_class = CatalogListPagination


class CatalogItemViewSet(mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """
    ViewSet for retrieving one specific catalog item.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"

