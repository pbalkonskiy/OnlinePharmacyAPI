from rest_framework import permissions


class IsCustomerOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            return obj.customer == request.user.customer
