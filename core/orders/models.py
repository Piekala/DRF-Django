"""Modelos do modulo de pedidos e pagamentos."""

from django.conf import settings
from django.db import models, transaction
from rest_framework.exceptions import ValidationError

from common.models import TimeStampedModel
from customers.models import Customer
from products.models import Product


class SalesOrder(TimeStampedModel):
    """Pedido de venda principal do sistema."""

    class Status(models.TextChoices):
        """Estados do ciclo de vida comercial do pedido."""

        DRAFT = 'draft', 'Rascunho'
        CONFIRMED = 'confirmed', 'Confirmado'
        PAID = 'paid', 'Pago'
        SHIPPED = 'shipped', 'Enviado'
        CANCELLED = 'cancelled', 'Cancelado'

    STATUS_TRANSITIONS = {
        Status.DRAFT: {Status.CONFIRMED, Status.CANCELLED},
        Status.CONFIRMED: {Status.PAID, Status.CANCELLED},
        Status.PAID: {Status.SHIPPED, Status.CANCELLED},
        Status.SHIPPED: set(),
        Status.CANCELLED: set(),
    }

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    salesperson = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sales_orders',
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    expected_delivery = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """Texto amigavel para o admin e logs de depuracao."""
        return f'Pedido #{self.pk} - {self.customer.company_name}'

    def can_transition(self, new_status):
        if self.status == new_status:
            return True
        return new_status in self.STATUS_TRANSITIONS.get(self.status, set())

    def _reserve_stock(self):
        for item in self.items.select_related('product').select_for_update():
            product = item.product
            if product.stock < item.quantity:
                raise ValidationError({'items': [f'Estoque insuficiente para {product.name}.']})
            product.stock -= item.quantity
            product.save(update_fields=['stock', 'updated_at'])

    def _release_stock(self):
        for item in self.items.select_related('product').select_for_update():
            product = item.product
            product.stock += item.quantity
            product.save(update_fields=['stock', 'updated_at'])

    @transaction.atomic
    def transition_to(self, new_status):
        if not self.can_transition(new_status):
            raise ValidationError({'status': f'Transicao invalida: {self.status} -> {new_status}.'})

        if self.status == self.Status.DRAFT and new_status == self.Status.CONFIRMED:
            self._reserve_stock()
        if self.status in {self.Status.CONFIRMED, self.Status.PAID} and new_status == self.Status.CANCELLED:
            self._release_stock()

        self.status = new_status
        self.save(update_fields=['status', 'updated_at'])
        return self


class SalesOrderItem(TimeStampedModel):
    """Item pertencente a um pedido com preco congelado na venda."""

    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        """Representacao amigavel do item."""
        return f'{self.order_id} - {self.product.name}'


class PaymentTransaction(TimeStampedModel):
    """Registro simplificado de uma tentativa de pagamento."""

    class Status(models.TextChoices):
        """Estado do processamento do pagamento."""

        PENDING = 'pending', 'Pendente'
        APPROVED = 'approved', 'Aprovado'
        FAILED = 'failed', 'Falhou'

    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='payments')
    provider = models.CharField(max_length=60)
    external_id = models.CharField(max_length=120, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        previous_status = None
        if self.pk and PaymentTransaction.objects.filter(pk=self.pk).exists():
            previous_status = PaymentTransaction.objects.get(pk=self.pk).status

        result = super().save(*args, **kwargs)

        if self.status == self.Status.APPROVED and previous_status != self.Status.APPROVED:
            self.order.transition_to(SalesOrder.Status.PAID)

        return result

    def __str__(self):
        """Representacao amigavel da transacao."""
        return f'Pagamento {self.provider} - pedido #{self.order_id}'
