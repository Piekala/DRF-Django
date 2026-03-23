"""Views DRF do modulo de contas."""

from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from accounts.permissions import IsAdminProfile
from accounts.selectors import users_with_profile
from accounts.services import get_or_create_profile
from accounts.api.serializers import CurrentUserSerializer, UserCreateSerializer, UserSerializer


class LoginView(ObtainAuthToken):
    """Endpoint padrao de login por token."""

    permission_classes = [permissions.AllowAny]


class UserListCreateView(generics.ListCreateAPIView):
    """Lista e cria usuarios, restrito ao perfil administrativo."""

    queryset = users_with_profile()
    permission_classes = [IsAdminProfile]

    def get_serializer_class(self):
        """Troca o serializer conforme a operacao de leitura ou escrita."""
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer


class MeView(generics.RetrieveAPIView):
    """Retorna os dados do usuario autenticado sem buscar por ID na URL."""

    serializer_class = CurrentUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Usa o usuario da sessao/token atual como objeto da view."""
        get_or_create_profile(self.request.user)
        return self.request.user

    def get(self, request, *args, **kwargs):
        """Mantem a resposta explicita para ficar didatico no estudo."""
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)
