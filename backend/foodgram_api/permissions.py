from rest_framework import permissions


class OwnerAdminReadOnly(permissions.BasePermission):
    message = "You can't edit this post"

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user and request.user.is_staff
        )
