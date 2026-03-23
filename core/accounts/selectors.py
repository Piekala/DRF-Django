"""Consultas reutilizaveis do modulo de contas."""

from django.contrib.auth import get_user_model


def users_with_profile():
    """Retorna usuarios ja preparados com select_related no perfil."""
    return get_user_model().objects.select_related('profile').order_by('username')
