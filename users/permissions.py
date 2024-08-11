from rest_framework import permissions


class IsModeratorOrOwner(permissions.BasePermission):
    """
    Разрешение, позволяющее доступ только владельцам объекта или модераторам.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_staff


class IsModeratorOrSuperuser(permissions.BasePermission):
    """
    Разрешение, позволяющее доступ только модераторам или суперпользователям.
    """

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.id:
            return True
        return "Вы не обладаете достаточными правами для данного действия"
