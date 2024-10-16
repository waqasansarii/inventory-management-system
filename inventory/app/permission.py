from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Allow access if the user is an admin or a moderator.
    """
    def has_permission(self, request, view):
        
        return request.user.is_superuser