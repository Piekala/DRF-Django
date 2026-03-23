"""Configuracao da app que concentra componentes compartilhados."""

from django.apps import AppConfig


class CommonConfig(AppConfig):
    """Registra a app common no Django."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'
