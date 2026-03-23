"""Configuracao da app de produtos."""

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Registra o modulo de catalogo no Django."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
