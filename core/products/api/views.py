"""Views DRF do modulo de produtos."""

from rest_framework import permissions, response, status, viewsets
from rest_framework.decorators import action

from products.api.serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductStockAdjustmentSerializer,
    SupplierSerializer,
)
from products.services import low_stock_queryset, update_stock
from products.selectors import categories_queryset, products_queryset, suppliers_queryset


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD completo de categorias."""

    queryset = categories_queryset()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ('name', 'slug')


class SupplierViewSet(viewsets.ModelViewSet):
    """CRUD completo de fornecedores."""

    queryset = suppliers_queryset()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ('name', 'email')


class ProductViewSet(viewsets.ModelViewSet):
    """CRUD de produtos com acoes extras para operacoes comuns."""

    queryset = products_queryset()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ('name', 'sku', 'description')
    ordering_fields = ('name', 'price', 'stock', 'created_at')

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Lista produtos abaixo do nivel minimo de estoque."""
        queryset = low_stock_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def adjust_stock(self, request, pk=None):
        """Atualiza estoque de forma controlada e validada."""
        product = self.get_object()
        input_serializer = ProductStockAdjustmentSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        serializer = self.get_serializer(
            update_stock(product=product, quantity=input_serializer.validated_data['stock'])
        )
        return response.Response(serializer.data, status=status.HTTP_200_OK)
