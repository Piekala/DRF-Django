"""Configuracao da app de contas e perfis."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Registra a app e conecta sinais na inicializacao do Django."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        """Importa sinais para garantir cadastro automatico de perfil."""
        import accounts.signals  # noqa: F401
