import os
import stripe

from rest_framework import generics
from rest_framework import status
from rest_framework import mixins
from rest_framework import response
from rest_framework import filters

from django.urls import reverse
from django.shortcuts import redirect
from django.forms import model_to_dict

from order.models import Order
from order.tasks import check_order_payment_status
from order.stripe import create_stripe_order, confirm_payment_by_session
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
    """
    serializer_class = SimpleOrderSerializer
    permission_classes = (
        IsCustomerOwner,
    )

    filter_backends = (
        filters.OrderingFilter,
    )
    ordering = ("in_progress",)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(customer_id=self.kwargs["pk"], closed=False).all()


class OrderClosedListView(mixins.ListModelMixin,
                          generics.GenericAPIView):
    """
    Lists all closed archived orders.
    """
    serializer_class = SimpleOrderSerializer
    permission_classes = (
        IsCustomerOwner,
    )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(customer_id=self.kwargs["pk"], closed=True).all()


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
            {"Already collected": "Order is already checked out and paid"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, *args, **kwargs):
        order = self.get_object()

        if order.in_progress or order.is_paid:
            return response.Response(
                {"Order already ready": "Can't edit order's parameters"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return redirect(reverse("order_retrieve_url", args=[order.customer.id, order.id]))

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
        """
        POST request initializes new Stripe payment session and redirects customer to the
        Stripe's side to make a card transaction.

        Here 'is_paid' & 'payment_status' fields of the current order are switched to the appropriate
        values to pass the order to further management and stop Celery order deletion tasks.
        """
        order = self.get_object()

        if order.in_progress and not order.is_paid:
            data = model_to_dict(order)
            order.stripe_payment_id, order.stripe_order_id = create_stripe_order(data, order.total_price, order.key,
                                                                                 order.customer.user.first_name,
                                                                                 order.customer.user.last_name)
            order.save()

            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
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
                    mode="payment",
                    success_url="{}/{}/".format(ORDERS_URL, self.kwargs["pk"]),
                    cancel_url="{}/{}/".format(ORDERS_URL, self.kwargs["pk"])
                )

                session_id = checkout_session.id
                if confirm_payment_by_session(session_id):

                    # Payment confirmation based on the session, but not on the 'payment_intent' parameter,
                    # that session gets after a successful payment. Bugs based on order 'is_paid' and 'payment_status'
                    # field values are allowed in case the payment process was interrupted or in case of any other
                    # issues.

                    order.is_paid = True
                    order.payment_status = "Successfully paid"
                    order.save()
                    return redirect(checkout_session.url, code=status.HTTP_201_CREATED)

                else:
                    return response.Response({"Payment error": "Payment session unsuccessful"},
                                             status=status.HTTP_402_PAYMENT_REQUIRED)

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
