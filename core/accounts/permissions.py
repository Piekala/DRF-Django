"""Permissoes customizadas da API de contas."""

from rest_framework.permissions import BasePermission

from accounts.models import UserProfile


class IsAdminProfile(BasePermission):
    """Libera acesso apenas para usuarios autenticados com papel administrativo."""

    def has_permission(self, request, view):
        """Aceita staff/superuser nativos ou perfil de negocio ADMIN."""
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        return getattr(getattr(user, 'profile', None), 'role', None) == UserProfile.Role.ADMIN
