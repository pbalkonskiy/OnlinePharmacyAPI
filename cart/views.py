from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import response

from cart.models import Cart, Position
from cart.serializers import (CartSerializer,
                              PositionSerializer,
                              UpdatePositionSerializer)

from order.models import Order
from order.serializers import OrderSerializer


class CartRetrieveDeleteAllPositionsView(mixins.RetrieveModelMixin,
                                         mixins.CreateModelMixin,
                                         mixins.DestroyModelMixin,
                                         generics.GenericAPIView):
    """
    View that retrieves user's cart based on 'CartSerializer', so it also
    provides cart ID, total positions number and total price (GET).

    Among other things, the view gives the ability to erase all items from the cart.

    The key function of the view is to create a customer order based on the added product positions.
    """

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (
        permissions.AllowAny,
    )

    def get(self, request, *args, **kwargs):
        """
        Provides data from the specific cart object based on 'CartSerializer'.
        """
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Used to create new record in the 'Order' model filled with added cart positions.
        """
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Used to create new 'Order' exemplar based on customer ID.
        """
        order = Order.objects.create(customer=request.user.customer)
        order.save()
        serializer = OrderSerializer(order)
        return response.Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        """
        Clears the cart or deletes all positions, related to the cart object
        using overridden 'destroy' method that returns cleared cart.
        """
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        cart_instance = self.get_object()
        serializer = self.get_serializer(cart_instance)
        for position in cart_instance.positions.all():
            position.delete()
        return response.Response(serializer.data)

    def get_serializer_class(self):
        method = self.request.method
        if method == "GET" or method == "DELETE":
            return self.serializer_class
        return OrderSerializer


class CartListUpdatePositionsView(mixins.ListModelMixin,
                                  mixins.UpdateModelMixin,
                                  generics.GenericAPIView):
    """
    View allows to observe the cart positions list based on the 'PositionSerializer'
    and to update one specific position's parameters using PATCH request method.
    """
    queryset = Cart.objects.all()
    permission_classes = (
        permissions.AllowAny,
    )

    def get(self, request, *args, **kwargs):
        """
        Lists data from positions related to the cart object.
        """
        return self.list(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Allows to update parameters of a specific position object from the cart.
        """
        return self.partial_update(request, *args, **kwargs)

    def get_queryset(self):
        return Position.objects.filter(cart_id=self.kwargs["pk"]).all()

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdatePositionSerializer
        return PositionSerializer

    def get_serializer_context(self):
        return {
            "user_id": self.kwargs["pk"]
        }


class CartDeletePositionsView(mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin,
                              generics.GenericAPIView):
    """
    View retrieves one position from the cart. Allows to delete it from the cart.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (
        permissions.AllowAny,
    )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
