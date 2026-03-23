"""Modelos do modulo de armazens e remessas."""

from django.db import models

from common.models import TimeStampedModel
from orders.models import SalesOrder, SalesOrderItem


class Warehouse(TimeStampedModel):
    """Centro de distribuicao de onde as remessas saem."""

    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        """Nome amigavel do armazem."""
        return self.name


class Shipment(TimeStampedModel):
    """Remessa associada a um pedido e a um armazem."""

    class Status(models.TextChoices):
        """Etapas logisticas simplificadas para o exemplo."""

        PENDING = 'pending', 'Pendente'
        PICKING = 'picking', 'Separacao'
        IN_TRANSIT = 'in_transit', 'Em transito'
        DELIVERED = 'delivered', 'Entregue'

    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='shipments')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='shipments')
    tracking_code = models.CharField(max_length=40, unique=True)
    carrier = models.CharField(max_length=80)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    dispatched_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """Codigo de rastreio exibido em telas administrativas."""
        return self.tracking_code


class ShipmentItem(TimeStampedModel):
    """Relaciona uma remessa com itens especificos do pedido."""

    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='items')
    order_item = models.ForeignKey(SalesOrderItem, on_delete=models.PROTECT, related_name='shipment_items')
    quantity = models.PositiveIntegerField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        """Representacao amigavel do item enviado."""
        return f'{self.shipment.tracking_code} - item {self.order_item_id}'
