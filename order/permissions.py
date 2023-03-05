from rest_framework import permissions


class IsDELIVERYManager(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            is_delivery_manager = request.user.employee.position == "delivery manager"

        except AttributeError:
            is_delivery_manager = False
        if request.user.is_superuser or is_delivery_manager:
            return True
        return False


class IsSELLERManager(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            is_delivery_manager = request.user.employee.position == "seller manager"
        except AttributeError:
            is_delivery_manager = False
        if request.user.is_superuser or is_delivery_manager:
            return True
        return False
