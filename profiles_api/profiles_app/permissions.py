from rest_framework import permissions


class UserProfilePermission(permissions.BasePermission):
    """To given permission to update / view profile

    Args:
        permissions (Permission): Base permission provided by rest framework
    """
    def has_object_permission(self, request, view, object):
        """Checks whether user have a permission to view or update profile

        Args:
            request (HTTPRequest): Input request
            object (User): User object to be viewed / updated
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return object.id == request.user.id