"""Regras de negocio do modulo de contas."""

from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import UserProfile


@transaction.atomic
def create_user_with_profile(*, username, email, password, role, phone='', department='', bio=''):
    """Cria usuario e sincroniza os dados complementares do perfil."""
    user_model = get_user_model()
    user = user_model.objects.create_user(username=username, email=email, password=password)
    UserProfile.objects.update_or_create(
        user=user,
        defaults={
            'role': role,
            'phone': phone,
            'department': department,
            'bio': bio,
        },
    )
    return user


def get_or_create_profile(user):
    """Garante que um usuario antigo tambem tenha perfil associado."""
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile
