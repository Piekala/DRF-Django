"""Rotas do modulo de contas."""

from django.urls import path

from accounts.api.views import LoginView, MeView, UserListCreateView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('me/', MeView.as_view(), name='me'),
]
