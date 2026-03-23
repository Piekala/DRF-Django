"""Regras de negocio do modulo de clientes."""

from customers.models import CustomerAddress


def ensure_single_main_address(customer, current_address=None):
    """Garante que apenas um endereco por cliente fique marcado como principal."""
    if current_address and current_address.is_main:
        CustomerAddress.objects.filter(customer=customer).exclude(pk=current_address.pk).update(is_main=False)
