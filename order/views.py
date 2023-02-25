from rest_framework import generics
from rest_framework import status
from rest_framework import mixins
from rest_framework import response

from order.models import Order
from order.tasks import check_order_payment_status
from order.serializers import (OrderSerializer,
                               SimpleOrderSerializer,
                               CheckOutOrderSerializer,
                               AddOrderSerializer)

from cart.permissions import IsCustomerOwner


class OrderListView(mixins.ListModelMixin,
                    generics.GenericAPIView):
    """
    Pass.
    """
    serializer_class = SimpleOrderSerializer
    permission_classes = (
        IsCustomerOwner,
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(customer_id=self.kwargs["pk"]).all()


class OrderRetrieveCheckOutDeleteView(mixins.RetrieveModelMixin,
                                      mixins.CreateModelMixin,
                                      mixins.UpdateModelMixin,
                                      mixins.DestroyModelMixin,
                                      generics.GenericAPIView):
    """
    Pass.
    """
    serializer_class = OrderSerializer
    permission_classes = (
        IsCustomerOwner,
    )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Returns nothing, just changes 'in_progress' order field to True.
        Contains 'check_order_payment_status' Celery task.
        """
        order = self.get_object()

        if order.delivery_method and order.payment_method and order.payment_status:
            order.in_progress = True
            order.save()

            serializer = self.get_serializer(order)
            check_order_payment_status.delay(order.id)
            return response.Response(serializer.data)

        return response.Response(
            {"Order unfulfilled": "Additional information required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        method = self.request.method
        if method == "PATCH":
            return CheckOutOrderSerializer
        if method == "POST":
            return AddOrderSerializer
        return self.serializer_class

    def get_queryset(self):
        return Order.objects.filter(customer_id=self.kwargs["pk"]).all()
