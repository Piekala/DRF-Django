"""Configuracao da app de expedicao e armazens."""

from django.apps import AppConfig


class ShippingConfig(AppConfig):
    """Registra o modulo logistico no Django."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shipping'
