from rest_framework import permissions


class UserProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, object):
        return request.method in permissions.SAFE_METHODS or request.user.id == object.id

class UserScoreTablePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, object):
        return request.method in permissions.SAFE_METHODS or object.user.id == request.user.id