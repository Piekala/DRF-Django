"""Modelos do catalogo de produtos e fornecedores."""

from django.db import models

from common.models import TimeStampedModel


class Category(TimeStampedModel):
    """Agrupa produtos por tipo ou familia comercial."""

    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        """Nome exibido em listas e no Django admin."""
        return self.name


class Supplier(TimeStampedModel):
    """Representa o fornecedor responsavel pelo produto."""

    name = models.CharField(max_length=140)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    lead_time_days = models.PositiveIntegerField(default=7)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        """Nome amigavel do fornecedor."""
        return self.name


class Product(TimeStampedModel):
    """Produto vendavel no catalogo B2B."""

    class Status(models.TextChoices):
        """Estados simples para controlar disponibilidade comercial."""

        DRAFT = 'draft', 'Rascunho'
        ACTIVE = 'active', 'Ativo'
        ARCHIVED = 'archived', 'Arquivado'

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=120)
    sku = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=5)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        """Nome exibido em logs, admin e shell."""
        return self.name

    @property
    def needs_restock(self):
        """Sinaliza quando o estoque ficou abaixo do nivel de reposicao."""
        return self.stock <= self.reorder_level
