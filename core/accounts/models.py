"""Modelos do modulo de contas."""

from django.conf import settings
from django.db import models

from common.models import TimeStampedModel


class UserProfile(TimeStampedModel):
    """Complementa o usuario padrao do Django com dados de negocio."""

    class Role(models.TextChoices):
        """Perfis simples para demonstrar autorizacao por papel."""

        ADMIN = 'admin', 'Administrador'
        SALES = 'sales', 'Comercial'
        OPERATIONS = 'operations', 'Operacoes'
        ANALYST = 'analyst', 'Analista'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ANALYST)
    phone = models.CharField(max_length=30, blank=True)
    department = models.CharField(max_length=80, blank=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        """Representacao amigavel no admin e no shell."""
        return f'Perfil de {self.user.username}'
