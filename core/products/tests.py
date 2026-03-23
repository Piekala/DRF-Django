"""Testes do modulo de produtos."""

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from products.models import Category, Product, Supplier


class ProductApiTests(APITestCase):
    """Cobre criacao de produto e validacao de ajuste de estoque."""

    def setUp(self):
        """Cria usuario autenticado e entidades base do catalogo."""
        self.user = get_user_model().objects.create_user(username='tester', password='12345678')
        self.client.force_authenticate(self.user)
        self.category = Category.objects.create(name='Notebooks', slug='notebooks')
        self.supplier = Supplier.objects.create(name='Distribuidora Central')

    def test_can_create_product(self):
        """Confirma o fluxo basico de cadastro de produto via API."""
        response = self.client.post(
            '/api/v1/products/products/',
            {
                'category': self.category.id,
                'supplier': self.supplier.id,
                'name': 'Notebook Pro 14',
                'sku': 'NB-PRO-14',
                'description': 'Equipamento para times comerciais.',
                'price': '8500.00',
                'cost': '6200.00',
                'stock': 12,
                'reorder_level': 3,
                'status': 'active',
                'is_published': True,
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)

    def test_adjust_stock_rejects_negative_values(self):
        """Garante resposta 400 quando o ajuste de estoque e invalido."""
        product = Product.objects.create(
            category=self.category,
            supplier=self.supplier,
            name='Notebook Pro 16',
            sku='NB-PRO-16',
            price='9500.00',
            cost='7000.00',
            stock=8,
        )
        response = self.client.post(
            f'/api/v1/products/products/{product.id}/adjust_stock/',
            {'stock': -3},
            format='json',
        )
        self.assertEqual(response.status_code, 400)
