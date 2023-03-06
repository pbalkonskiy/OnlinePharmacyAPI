from rest_framework import permissions


class IsCustomerOrReadOnly(permissions.BasePermission):
    """
    Allows 'AnonymousUser' users only to use GET methods. Customers allowed to use POST also.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(request.user, "customer"):
            return True
        return False


class IsStuffOrEmployee(permissions.BasePermission):
    """
    Allows only superusers or 'Employee' type users to create new products for the catalog.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser or hasattr(request.user, "employee"):
            return True
        return False


class IsStuffOrEmployeeOrReadOnly(permissions.BasePermission):
    """
    For 'Customer' users only allows to observe product exemplar using GET.
    'Employee' type users and superusers allowed to update or delete products.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser or hasattr(request.user, "employee"):
            return True
        return False


class IsProductManagerOrCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'employee') and request.user.employee.position == "content manager":
            return True
        if hasattr(request.user, "customer"):
            return True
        return False
