"""Consultas reutilizaveis do modulo de produtos."""

from products.models import Category, Product, Supplier


def categories_queryset():
    """Lista categorias ordenadas alfabeticamente."""
    return Category.objects.order_by('name')


def suppliers_queryset():
    """Lista fornecedores ordenados alfabeticamente."""
    return Supplier.objects.order_by('name')


def products_queryset():
    """Retorna produtos com joins comuns ja resolvidos."""
    return Product.objects.select_related('category', 'supplier').order_by('name')
