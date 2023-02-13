from django.shortcuts import render
from rest_framework import generics, permissions, mixins

from users.models import Customer, CommonUser
from users.serializers import CustomerSerializer, CommonUserSerializer


# Create your views here.

class CustomerViewList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = permissions.IsAdminUser,

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CustomerCreateView(mixins.RetrieveModelMixin, generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (
        permissions.AllowAny,
    )


class CustomerRetrieveUpdateDeleteView(mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin,
                                       generics.GenericAPIView):
    queryset = Customer.objects.all()
    lookup_field = 'email'
    serializer_class = CustomerSerializer
    permission_classes = (
        permissions.AllowAny,
    )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
