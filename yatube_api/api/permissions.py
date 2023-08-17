from rest_framework import permissions


class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Проверяет является ли отправитель запроса автором определенного поста.
    """

    def has_permission(self, request, view):
        """Фунцкия для проверки запроса от различных пользователей."""
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Фунцкия для проверки пользователя."""
        return bool(
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
