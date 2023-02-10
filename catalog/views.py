from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions

from catalog.models import Product
from catalog.serializers import (SimpleProductSerializer,
                                 ProductSerializer)
from catalog.paginations import CatalogListPagination
from catalog.permissions import IsAdminOrStuff


class CatalogListView(mixins.ListModelMixin,
                      generics.GenericAPIView):
    """
    View for browsing the catalog as a list of products.
    """
    queryset = Product.objects.all()
    serializer_class = SimpleProductSerializer
    pagination_class = CatalogListPagination
    permission_classes = (
        permissions.AllowAny,
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CatalogRetrieveUpdateDeleteView(mixins.RetrieveModelMixin,
                                      mixins.UpdateModelMixin,
                                      mixins.DestroyModelMixin,
                                      generics.GenericAPIView):
    """
    View for retrieving one specific catalog item for observing;
    updating or deleting catalog items by administration.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"
    permission_classes = (
        permissions.AllowAny,
    )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CatalogCreateItemView(mixins.CreateModelMixin,
                            generics.GenericAPIView):
    """
    View for creating, updating and deleting a product in catalog.
    Originally allowed for resource administrations & managers stuff only.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (
        IsAdminOrStuff,
    )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
