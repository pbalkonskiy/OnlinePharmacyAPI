import os
import stripe

from rest_framework import generics
from rest_framework import status
from rest_framework import mixins
from rest_framework import response
from rest_framework import views

from django.urls import reverse
from django.shortcuts import redirect
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from order.models import Order
from order.tasks import check_order_payment_status
from order.stripe import create_stripe_order
from order.serializers import (OrderSerializer,
                               SimpleOrderSerializer,
                               CheckOutOrderSerializer,
                               AddOrderSerializer)

from cart.permissions import IsCustomerOwner

stripe.api_key = os.environ["STRIPE_PRIVATE_KEY"]
ORDERS_URL = "http://127.0.0.1:8000/orders"


class OrderActiveListView(mixins.ListModelMixin,
                          generics.GenericAPIView):
    """
    Lists all customer's orders.
    Will be updated soon.
    """

    serializer_class = SimpleOrderSerializer
    permission_classes = (
        IsCustomerOwner,
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(customer_id=self.kwargs["pk"]).all()


class OrderRetrieveUpdateDeleteView(mixins.RetrieveModelMixin,
                                    mixins.CreateModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin,
                                    generics.GenericAPIView):
    """
    Retrieves one specific order. Allows to update editable parameters based on
    'CheckOutOrderSerializer' and delete the order.

    POST method turns 'in_progress' filed to True. Used to confirm the inputted order
    parameters and move to the payment system.
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
        Method for order unit confirmation. Redirects user to the checkout URL ('OrderCheckOutView').
        Changes 'in_progress' order field to True. Contains 'check_order_payment_status' Celery task.
        """

        order = self.get_object()
        if not order.is_paid:

            if order.delivery_method and order.payment_method and order.payment_status:
                order.in_progress = True
                order.save()
                check_order_payment_status.delay(order.id)

                pk = self.kwargs.get("pk")
                order_id = self.kwargs.get("id")
                redirect_url = reverse("checkout_url", kwargs={"pk": pk, "id": order_id})
                return redirect(redirect_url)

            return response.Response(
                {"Order unfulfilled": "Additional information required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return response.Response(
            {"Already collected": "Order is already checked out and awaits payment"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, *args, **kwargs):
        order = self.get_object()

        if order.in_progress or order.is_paid:
            return response.Response(
                {"Order already ready": "Can't edit order's parameters"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        patch_response = self.partial_update(request, *args, **kwargs)
        if patch_response.status_code == status.HTTP_200_OK:
            return redirect(reverse("order_retrieve_url", args=[order.customer.id, order.id]))

        return patch_response

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


class OrderCheckOutView(mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
    """
    View used to confirm edited order and dash to the payment or to use DELETE method
    for cancellation and coming back to the previous step on the 'OrderRetrieveUpdateDeleteView'.
    """

    serializer_class = OrderSerializer
    permission_classes = (
        IsCustomerOwner,
    )
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        order = self.get_object()

        if order.in_progress and not order.is_paid:
            data = model_to_dict(order, fields=["id", "customer"])
            order.stripe_payment_id, order.stripe_order_id = create_stripe_order(data, order.total_price)
            order.save()

            try:
                checkout_session = stripe.checkout.Session.create(
                    line_items=[
                        {
                            "price_data": {
                                "currency": "byn",
                                "unit_amount": int(order.total_price * 100),
                                "product_data": {
                                    "name": str(order.id)
                                }
                            },
                            "quantity": 1,
                        }
                    ],
                    metadata={
                        "product_id": order.stripe_order_id,
                    },
                    mode="payment",
                    success_url="{}/{}/".format(ORDERS_URL, self.kwargs["pk"]),
                    cancel_url="{}/{}/".format(ORDERS_URL, self.kwargs["pk"])
                )
                order.is_paid = True
                order.payment_status = "Successfully paid"
                order.save()
                return redirect(checkout_session.url, code=status.HTTP_201_CREATED)

            except Exception as exception:
                order.is_paid = False
                order.payment_status = "Pending payment"
                order.save()
                return response.Response({"Session error": str(exception)}, status=status.HTTP_406_NOT_ACCEPTABLE)

        return response.Response(
            {"Payment already closed": "You have already paid for the order and have no need to repeat again."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST":
            return AddOrderSerializer
        return self.serializer_class

    def get_queryset(self):
        return Order.objects.filter(customer_id=self.kwargs["pk"]).all()
