from rest_framework import permissions


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            #print("WTF HOW HOW HOW HOW HOW HOW HOW HOW HOW HOW HOW HOW HOW ")
            is_manager = request.user.employee.position == "content manager"

        except ValueError:
            is_manager = False
        if request.user.is_superuser or is_manager:
            return True
        return False
