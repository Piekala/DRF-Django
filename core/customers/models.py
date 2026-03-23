"""Modelos do modulo de clientes."""

from django.conf import settings
from django.db import models

from common.models import TimeStampedModel


class CustomerSegment(TimeStampedModel):
    """Segmenta clientes por perfil comercial ou porte."""

    name = models.CharField(max_length=80, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        """Nome amigavel do segmento."""
        return self.name


class Customer(TimeStampedModel):
    """Cadastro principal do cliente corporativo."""

    class Status(models.TextChoices):
        """Estado de relacionamento comercial do cliente."""

        LEAD = 'lead', 'Lead'
        ACTIVE = 'active', 'Ativo'
        INACTIVE = 'inactive', 'Inativo'

    segment = models.ForeignKey(CustomerSegment, on_delete=models.PROTECT, related_name='customers')
    account_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_customers',
    )
    company_name = models.CharField(max_length=140)
    document = models.CharField(max_length=30, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.LEAD)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['company_name']

    def __str__(self):
        """Nome exibido no admin e em logs."""
        return self.company_name


class CustomerAddress(TimeStampedModel):
    """Endereco de faturamento, entrega ou referencia do cliente."""

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=60)
    street = models.CharField(max_length=180)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=20)
    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = ['customer__company_name', '-is_main', 'label']
        constraints = [
            models.UniqueConstraint(
                fields=['customer'],
                condition=models.Q(is_main=True),
                name='unique_customer_main_address',
            )
        ]

    def __str__(self):
        """Representacao amigavel do endereco."""
        return f'{self.customer.company_name} - {self.label}'
