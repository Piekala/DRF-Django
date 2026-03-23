"""Configuracao da app de clientes."""

from django.apps import AppConfig


class CustomersConfig(AppConfig):
    """Registra o modulo de clientes no Django."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customers'
