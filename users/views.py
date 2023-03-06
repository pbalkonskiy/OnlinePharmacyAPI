from rest_framework import generics, mixins
from rest_framework import permissions

from users.models import Customer, Employee
from users.permissions import IsStaff, IsStaffOrOwner
from users.serializers import CustomerSerializer, EmployeeSerializer


# Create your views here.

class CustomerViewList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsStaff]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CustomerCreateView(mixins.RetrieveModelMixin, generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny]


class CustomerRetrieveUpdateDeleteView(mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin,
                                       generics.GenericAPIView):
    queryset = Customer.objects.all()
    lookup_field = 'slug'
    serializer_class = CustomerSerializer
    permission_classes = [IsStaffOrOwner]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class EmployeeViewList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [
        IsStaff
    ]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EmployeeCreateView(mixins.RetrieveModelMixin, generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [
        permissions.IsAdminUser
    ]


class EmployeeRetrieveUpdateDeleteView(mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin,
                                       generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsStaffOrOwner]
    lookup_field = "slug"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
