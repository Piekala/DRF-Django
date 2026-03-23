"""Testes do modulo de pedidos."""

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from customers.models import Customer, CustomerSegment
from orders.models import SalesOrder
from products.models import Category, Product, Supplier


class OrdersApiTests(APITestCase):
    """Valida criacao de pedido e protecoes de integridade comercial."""

    def setUp(self):
        """Cria cliente, produto e vendedor para os cenarios."""
        self.user = get_user_model().objects.create_user(username='pedido', password='12345678')
        self.client.force_authenticate(self.user)
        self.segment = CustomerSegment.objects.create(name='SMB')
        self.customer = Customer.objects.create(
            segment=self.segment,
            account_manager=self.user,
            company_name='Cliente XPTO',
            document='11.111.111/0001-11',
            status='active',
        )
        self.category = Category.objects.create(name='Acessorios', slug='acessorios')
        self.supplier = Supplier.objects.create(name='Fornecedor 1')
        self.product = Product.objects.create(
            category=self.category,
            supplier=self.supplier,
            name='Mouse sem fio',
            sku='MS-001',
            price='120.00',
            cost='70.00',
            stock=30,
        )

    def test_create_order_with_items(self):
        """Confirma o fluxo feliz de criacao de um pedido."""
        response = self.client.post(
            '/api/v1/orders/orders/',
            {
                'customer': self.customer.id,
                'salesperson': self.user.id,
                'status': 'draft',
                'shipping_fee': '20.00',
                'discount_amount': '10.00',
                'items': [{'product': self.product.id, 'quantity': 2, 'unit_price': '120.00'}],
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SalesOrder.objects.count(), 1)
        self.assertEqual(str(SalesOrder.objects.first().total_amount), '250.00')

    def test_rejects_tampered_price(self):
        """Impede que o cliente da API envie um preco adulterado."""
        response = self.client.post(
            '/api/v1/orders/orders/',
            {
                'customer': self.customer.id,
                'salesperson': self.user.id,
                'status': 'draft',
                'items': [{'product': self.product.id, 'quantity': 1, 'unit_price': '1.00'}],
            },
            format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_create_order_with_inactive_customer_is_rejected(self):
        """Cliente nao ativo nao deve poder gerar pedidos."""
        self.customer.status = 'inactive'
        self.customer.save()

        response = self.client.post(
            '/api/v1/orders/orders/',
            {
                'customer': self.customer.id,
                'salesperson': self.user.id,
                'status': 'draft',
                'items': [{'product': self.product.id, 'quantity': 1, 'unit_price': '120.00'}],
            },
            format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_order_status_transitions_invalid(self):
        """Nao e possivel pular estados de ciclo de venda."""
        response = self.client.post(
            '/api/v1/orders/orders/',
            {
                'customer': self.customer.id,
                'salesperson': self.user.id,
                'status': 'draft',
                'items': [{'product': self.product.id, 'quantity': 1, 'unit_price': '120.00'}],
            },
            format='json',
        )
        order_id = response.data['id']

        response = self.client.patch(
            f'/api/v1/orders/orders/{order_id}/',
            {'status': 'shipped'},
            format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_payment_approved_updates_order_to_paid(self):
        """Pagamento aprovado leva o pedido a status pago."""
        response = self.client.post(
            '/api/v1/orders/orders/',
            {
                'customer': self.customer.id,
                'salesperson': self.user.id,
                'status': 'confirmed',
                'items': [{'product': self.product.id, 'quantity': 2, 'unit_price': '120.00'}],
            },
            format='json',
        )
        order_id = response.data['id']

        response = self.client.post(
            '/api/v1/orders/payments/',
            {
                'order': order_id,
                'provider': 'dummy',
                'amount': '240.00',
                'status': 'approved',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)

        self.assertEqual(SalesOrder.objects.get(id=order_id).status, 'paid')

    def test_confirmed_order_reserves_stock_and_cancel_returns_stock(self):
        """Reservar e liberar estoque conforme status do pedido."""
        response = self.client.post(
            '/api/v1/orders/orders/',
            {
                'customer': self.customer.id,
                'salesperson': self.user.id,
                'status': 'confirmed',
                'items': [{'product': self.product.id, 'quantity': 5, 'unit_price': '120.00'}],
            },
            format='json',
        )
        order = SalesOrder.objects.first()
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 25)

        response = self.client.patch(
            f'/api/v1/orders/orders/{order.id}/',
            {'status': 'cancelled'},
            format='json',
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 30)
