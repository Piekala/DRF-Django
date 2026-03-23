"""Regras de negocio do modulo de pedidos."""

from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError

from orders.models import SalesOrder, SalesOrderItem
from customers.models import Customer
from products.models import Product


def _build_item_payload(items_data):
    """Normaliza e valida os itens recebidos antes de salvar no banco."""
    payload = []
    for item in items_data:
        product = item['product']
        quantity = item['quantity']

        # O backend define se o produto pode ou nao ser vendido neste momento.
        if product.status != Product.Status.ACTIVE or not product.is_published:
            raise ValidationError({'items': [f'O produto "{product.name}" nao esta disponivel para venda.']})
        # A API nao deve aceitar pedidos acima do estoque atual.
        if quantity > product.stock:
            raise ValidationError({'items': [f'Estoque insuficiente para "{product.name}".']})

        # O preco do pedido e congelado a partir do catalogo no momento da venda.
        unit_price = product.price
        line_total = Decimal(unit_price) * quantity
        payload.append(
            {
                'product': product,
                'quantity': quantity,
                'unit_price': unit_price,
                'line_total': line_total,
            }
        )
    return payload


def _validate_order_rules(order_data, payload):
    """Aplica invariantes do pedido antes de persistir a transacao."""
    customer = order_data['customer']
    if customer.status != Customer.Status.ACTIVE:
        raise ValidationError({'customer': 'Apenas clientes ativos podem receber pedidos.'})

    subtotal = sum((item['line_total'] for item in payload), Decimal('0'))
    shipping_fee = Decimal(order_data.get('shipping_fee', 0) or 0)
    discount_amount = Decimal(order_data.get('discount_amount', 0) or 0)
    if discount_amount > subtotal + shipping_fee:
        raise ValidationError({'discount_amount': 'O desconto nao pode exceder o valor total do pedido.'})


def _validate_status_transition(current_status, next_status):
    """Valida transicao de status do pedido."""
    if current_status == next_status:
        return
    if next_status not in SalesOrder.STATUS_TRANSITIONS.get(current_status, set()):
        raise ValidationError({'status': f'Transicao invalida: {current_status} -> {next_status}.'})


def recalculate_totals(order):
    """Recalcula subtotal e total final a partir dos itens persistidos."""
    subtotal = sum((item.line_total for item in order.items.all()), Decimal('0'))
    order.subtotal = subtotal
    order.total_amount = subtotal + order.shipping_fee - order.discount_amount
    order.save(update_fields=['subtotal', 'total_amount', 'updated_at'])
    return order


@transaction.atomic
def create_order(*, order_data, items_data):
    """Cria um pedido completo com seus itens em uma unica transacao."""
    requested_status = order_data.get('status', SalesOrder.Status.DRAFT)
    order_data['status'] = SalesOrder.Status.DRAFT

    payload = _build_item_payload(items_data)
    _validate_order_rules(order_data, payload)

    order = SalesOrder.objects.create(**order_data)
    SalesOrderItem.objects.bulk_create([SalesOrderItem(order=order, **item) for item in payload])
    order.refresh_from_db()
    order = recalculate_totals(order)

    if requested_status != SalesOrder.Status.DRAFT:
        order.transition_to(requested_status)

    return order


@transaction.atomic
def update_order(*, instance, order_data, items_data=None):
    """Atualiza pedido e, opcionalmente, substitui integralmente seus itens."""
    old_status = instance.status
    new_status = order_data.pop('status', old_status)
    _validate_status_transition(old_status, new_status)

    if items_data is not None and old_status in {
        SalesOrder.Status.CONFIRMED,
        SalesOrder.Status.PAID,
        SalesOrder.Status.SHIPPED,
    }:
        # Ajusta estoque antes da substituicao do item
        instance._release_stock()

    for field, value in order_data.items():
        setattr(instance, field, value)
    instance.save()

    if items_data is not None:
        payload = _build_item_payload(items_data)
        candidate_data = {
            'customer': order_data.get('customer', instance.customer),
            'shipping_fee': order_data.get('shipping_fee', instance.shipping_fee),
            'discount_amount': order_data.get('discount_amount', instance.discount_amount),
        }
        _validate_order_rules(candidate_data, payload)
        instance.items.all().delete()
        SalesOrderItem.objects.bulk_create([SalesOrderItem(order=instance, **item) for item in payload])

    else:
        _validate_order_rules(
            {
                'customer': order_data.get('customer', instance.customer),
                'shipping_fee': order_data.get('shipping_fee', instance.shipping_fee),
                'discount_amount': order_data.get('discount_amount', instance.discount_amount),
            },
            [
                {
                    'line_total': item.line_total,
                }
                for item in instance.items.all()
            ],
        )

    instance.refresh_from_db()
    instance = recalculate_totals(instance)

    if items_data is not None and old_status in {
        SalesOrder.Status.CONFIRMED,
        SalesOrder.Status.PAID,
        SalesOrder.Status.SHIPPED,
    }:
        instance._reserve_stock()

    if new_status != instance.status:
        instance.transition_to(new_status)

    return instance
