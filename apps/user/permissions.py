from rest_framework import permissions

class IsMe(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj or request.user.is_superuser

class IsMine(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.user or request.user.is_superuser
