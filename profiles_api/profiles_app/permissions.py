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
        return request.method in permissions.SAFE_METHODS or object.id == request.user.id


class ProfileFeedPermission(permissions.BasePermission):
    """Checks permissions to view or update feed

    Args:
        permissions (Permission): Base permission provided by rest framework
    """
    def has_object_permission(self, request, view, obj):
        """Checks whether user has a permission to read or update

        Args:
            request (HTTPRequest): Input Request
            obj (ProfileFeedItem): Profile feed item to be updated or viewed
        """
        return request.method in permissions.SAFE_METHODS or obj.user_profile.id == request.user.id