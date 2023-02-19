from rest_framework import generics, permissions, mixins
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from users.models import Customer, Employee
from users.serializers import CustomerSerializer, EmployeeSerializer


# Create your views here.

class CustomerViewList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = permissions.AllowAny,  # need to be AdminUser

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
    lookup_field = 'slug'
    serializer_class = CustomerSerializer
    permission_classes = (
        permissions.AllowAny,
        # permissions.IsAdminUser
    )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




class EmployeeViewList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (AllowAny,)  # need to be AdminUser

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



class EmployeeCreateView(mixins.RetrieveModelMixin, generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (AllowAny,)


class EmployeeRetrieveUpdateDeleteView(mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin,
                                       generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (permissions.AllowAny,)  # need to be AdminUser and current_user
    lookup_field = "slug"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ClSAP(generics.GenericAPIView):
    pass
