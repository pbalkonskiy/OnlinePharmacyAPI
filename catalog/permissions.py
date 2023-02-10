from rest_framework import permissions

from users.models import Employee


class IsAdminOrStuff(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        """Permission for employees (Employee table) and superusers to create, update and."""
        return isinstance(request.user.employee, Employee) or request.user.is_staff
