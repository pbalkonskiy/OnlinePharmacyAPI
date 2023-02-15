from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import response

from cart.models import Cart, Position
from cart.serializers import CartSerializer


class CartRetrieveUpdateClearView(mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin,
                                  generics.GenericAPIView):
    """
    Cart retrieve info, update and clear view. Originally allowed for
    customer (owner) and administration.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (
        permissions.AllowAny,
    )

    def get(self, request, *args, **kwargs):
        """
        Returns (retrieves) data from the cart object with ID passed to the URL.
        """
        return self.retrieve(request, *args, **kwargs)

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
            Position.objects.get(id=position.id).delete()
        return response.Response(serializer.data)
