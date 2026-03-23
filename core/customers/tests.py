"""Testes do modulo de clientes."""

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from customers.models import Customer, CustomerSegment


class CustomerApiTests(APITestCase):
    """Valida o cadastro basico de clientes pela API."""

    def setUp(self):
        """Cria usuario e segmento usados no cenario principal."""
        self.user = get_user_model().objects.create_user(username='vendas', password='12345678')
        self.client.force_authenticate(self.user)
        self.segment = CustomerSegment.objects.create(name='Enterprise')

    def test_create_customer(self):
        """Confirma que o endpoint cria um cliente valido."""
        response = self.client.post(
            '/api/v1/customers/customers/',
            {
                'segment': self.segment.id,
                'account_manager': self.user.id,
                'company_name': 'Alpha Tech',
                'document': '12.345.678/0001-99',
                'email': 'contato@alpha.com',
                'phone': '11999999999',
                'status': 'active',
                'credit_limit': '50000.00',
                'notes': 'Cliente piloto.',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Customer.objects.count(), 1)

    def test_single_main_address_per_customer(self):
        """Marca apenas um endereco principal por cliente."""
        customer = Customer.objects.create(
            segment=self.segment,
            account_manager=self.user,
            company_name='Beta Ltda',
            document='22.222.222/0001-22',
            status='active',
        )

        response1 = self.client.post(
            '/api/v1/customers/addresses/',
            {
                'customer': customer.id,
                'label': 'Matriz',
                'street': 'Rua A, 100',
                'city': 'Sao Paulo',
                'state': 'SP',
                'postal_code': '01000-000',
                'is_main': True,
            },
            format='json',
        )
        self.assertEqual(response1.status_code, 201)

        response2 = self.client.post(
            '/api/v1/customers/addresses/',
            {
                'customer': customer.id,
                'label': 'Filial',
                'street': 'Rua B, 200',
                'city': 'Campinas',
                'state': 'SP',
                'postal_code': '13000-000',
                'is_main': True,
            },
            format='json',
        )
        self.assertEqual(response2.status_code, 201)

        self.assertEqual(Customer.objects.first().addresses.filter(is_main=True).count(), 1)
