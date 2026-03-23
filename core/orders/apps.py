"""Configuracao da app de pedidos."""

from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """Registra o modulo de pedidos no Django."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
