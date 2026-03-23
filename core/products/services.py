"""Regras de negocio do modulo de produtos."""

from django.db.models import F

from products.models import Product


def low_stock_queryset():
    """Filtra produtos com estoque menor ou igual ao nivel de reposicao."""
    return Product.objects.filter(stock__lte=F('reorder_level')).select_related('category', 'supplier')


def update_stock(*, product, quantity):
    """Centraliza atualizacao manual de estoque em um unico ponto."""
    product.stock = quantity
    product.save(update_fields=['stock', 'updated_at'])
    return product
