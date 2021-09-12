from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.creator == request.user


class IsCreatorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.creator == request.user
        else:
            return request.user and request.user.is_authenticated


class IsCreatorOrAccessToEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            if obj.creator == request.user:
                return True
            if request.user in obj.access_edit.all():
                return True
        return False
