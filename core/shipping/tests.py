"""Testes do modulo de logistica."""

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from customers.models import Customer, CustomerSegment
from orders.models import SalesOrder, SalesOrderItem
from products.models import Category, Product, Supplier
from shipping.models import Warehouse


class ShippingApiTests(APITestCase):
    """Valida criacao de remessas e suas regras de integridade."""

    def setUp(self):
        """Cria pedido, itens e armazem usados nos cenarios."""
        self.user = get_user_model().objects.create_user(username='logistica', password='12345678')
        self.client.force_authenticate(self.user)
        self.segment = CustomerSegment.objects.create(name='Key Accounts')
        self.customer = Customer.objects.create(
            segment=self.segment,
            account_manager=self.user,
            company_name='Beta',
            document='22.222.222/0001-22',
            status='active',
        )
        self.category = Category.objects.create(name='Monitores', slug='monitores')
        self.supplier = Supplier.objects.create(name='Supplier')
        self.product = Product.objects.create(
            category=self.category,
            supplier=self.supplier,
            name='Monitor 27',
            sku='MON-27',
            price='1400.00',
            cost='900.00',
            stock=8,
        )
        self.order = SalesOrder.objects.create(
            customer=self.customer,
            salesperson=self.user,
            status=SalesOrder.Status.CONFIRMED,
        )
        self.order_item = SalesOrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            unit_price='1400.00',
            line_total='1400.00',
        )
        self.other_order = SalesOrder.objects.create(customer=self.customer, salesperson=self.user)
        self.other_order_item = SalesOrderItem.objects.create(
            order=self.other_order,
            product=self.product,
            quantity=1,
            unit_price='1400.00',
            line_total='1400.00',
        )
        self.warehouse = Warehouse.objects.create(name='CD Sao Paulo', code='SP01', city='Sao Paulo', state='SP')

    def test_create_shipment(self):
        """Confirma o fluxo feliz de criacao de uma remessa."""
        response = self.client.post(
            '/api/v1/shipping/shipments/',
            {
                'order': self.order.id,
                'warehouse': self.warehouse.id,
                'tracking_code': 'TRACK123',
                'carrier': 'Transporte X',
                'status': 'pending',
                'items': [{'order_item': self.order_item.id, 'quantity': 1}],
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)

    def test_rejects_order_item_from_another_order(self):
        """Impede vincular item de um pedido diferente na remessa atual."""
        response = self.client.post(
            '/api/v1/shipping/shipments/',
            {
                'order': self.order.id,
                'warehouse': self.warehouse.id,
                'tracking_code': 'TRACK999',
                'carrier': 'Transporte X',
                'status': 'pending',
                'items': [{'order_item': self.other_order_item.id, 'quantity': 1}],
            },
            format='json',
        )
        self.assertEqual(response.status_code, 400)
