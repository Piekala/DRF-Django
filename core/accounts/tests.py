"""Testes do modulo de contas cobrindo autenticacao e permissao."""

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import UserProfile


class AccountsApiTests(APITestCase):
    """Valida endpoints de perfil e restricao de acesso administrativo."""

    def setUp(self):
        """Cria usuarios e tokens usados pelos cenarios do teste."""
        self.user = get_user_model().objects.create_user(username='maria', password='12345678')
        self.user.profile.role = 'admin'
        self.user.profile.save(update_fields=['role', 'updated_at'])
        self.token = Token.objects.create(user=self.user)
        self.regular_user = get_user_model().objects.create_user(username='joao', password='12345678')

    def test_me_endpoint_returns_profile(self):
        """Confirma que o endpoint /me devolve o usuario autenticado."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/accounts/me/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'maria')

    def test_regular_user_cannot_list_users(self):
        """Impede que usuarios comuns consultem a lista completa de contas."""
        regular_token = Token.objects.create(user=self.regular_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {regular_token.key}')
        response = self.client.get('/api/v1/accounts/users/')
        self.assertEqual(response.status_code, 403)
