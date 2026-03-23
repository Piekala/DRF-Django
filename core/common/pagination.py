"""Paginacao padrao usada em todas as listagens da API."""

from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    """Permite paginacao simples com tamanho customizavel por querystring."""

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
