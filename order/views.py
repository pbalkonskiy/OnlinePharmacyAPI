from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions

from order.models import Order
from order.serializers import (OrderSerializer,
                               SimpleOrderSerializer,
                               CheckOutOrderSerializer)


class OrderListView(mixins.ListModelMixin,
                    generics.GenericAPIView):
    """
    Pass.
    """
    serializer_class = SimpleOrderSerializer
    permission_classes = (
        permissions.AllowAny,
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(customer_id=self.kwargs["pk"]).all()


class OrderRetrieveCheckOutDeleteView(mixins.RetrieveModelMixin,
                                      mixins.UpdateModelMixin,
                                      mixins.DestroyModelMixin,
                                      generics.GenericAPIView):
    """
    Pass.
    """
    serializer_class = OrderSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Method specially for user to pick suitable order parameters.
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        method = self.request.method
        if method == "PATCH":
            return CheckOutOrderSerializer
        return self.serializer_class

    def get_queryset(self):
        return Order.objects.filter(customer_id=self.kwargs["pk"]).all()
