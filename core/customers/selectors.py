"""Consultas reutilizaveis do modulo de clientes."""

from customers.models import Customer, CustomerAddress, CustomerSegment


def customer_segments_queryset():
    """Lista segmentos ordenados pelo nome."""
    return CustomerSegment.objects.order_by('name')


def customers_queryset():
    """Retorna clientes com relacoes comuns carregadas para a API."""
    return Customer.objects.select_related('segment', 'account_manager').prefetch_related('addresses')


def customer_addresses_queryset():
    """Retorna enderecos com o cliente ja resolvido."""
    return CustomerAddress.objects.select_related('customer')
