from rest_framework import permissions


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return True if (request.user.is_staff or request.user.is_superuser) else False


class IsStaffOrOwner(permissions.BasePermission):
    """
    Custom permission to only allow admins or owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
