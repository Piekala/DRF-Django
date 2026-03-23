"""Regras de negocio do modulo de logistica."""

from shipping.models import ShipmentItem


def build_shipment_items(shipment, items_data):
    """Cria os itens da remessa em lote para reduzir queries."""
    return ShipmentItem.objects.bulk_create([ShipmentItem(shipment=shipment, **item) for item in items_data])
