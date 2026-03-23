"""Consultas reutilizaveis do modulo de logistica."""

from shipping.models import Shipment, Warehouse


def warehouses_queryset():
    """Lista armazens em ordem alfabetica."""
    return Warehouse.objects.order_by('name')


def shipments_queryset():
    """Retorna remessas com joins prontos para a API."""
    return Shipment.objects.select_related('order', 'warehouse').prefetch_related('items__order_item__product')
