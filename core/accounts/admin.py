"""Configuracao do Django admin para o modulo de contas."""

from django.contrib import admin

from accounts.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Define como perfis aparecem para administradores no painel."""

    list_display = ('user', 'role', 'department', 'phone', 'created_at')
    list_filter = ('role', 'department')
    search_fields = ('user__username', 'user__email', 'department')
