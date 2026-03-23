"""Consultas reutilizaveis do modulo de pedidos."""

from orders.models import PaymentTransaction, SalesOrder


def sales_orders_queryset():
    """Retorna pedidos com cliente, vendedor, itens e pagamentos preparados."""
    return SalesOrder.objects.select_related('customer', 'salesperson').prefetch_related('items__product', 'payments')


def payments_queryset():
    """Retorna pagamentos com o pedido carregado."""
    return PaymentTransaction.objects.select_related('order')
