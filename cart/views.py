from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import response

from cart.models import Cart, Position
from cart.serializers import (CartSerializer,
                              PositionSerializer,
                              AddPositionSerializer)


class CartRetrieveUpdateClearView(mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
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
        Lists data from positions related to the cart object.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Used to add new / update previously added positions related to the cart.
        """
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return Position.objects.filter(cart_id=self.kwargs["pk"]).all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddPositionSerializer
        return PositionSerializer

    def get_serializer_context(self):
        return {
            "cart_id": self.kwargs["pk"]
        }

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
