"""Views DRF do modulo de pedidos."""

from rest_framework import permissions, viewsets

from orders.api.serializers import PaymentTransactionSerializer, SalesOrderSerializer
from orders.selectors import payments_queryset, sales_orders_queryset


class SalesOrderViewSet(viewsets.ModelViewSet):
    """CRUD completo de pedidos de venda."""

    queryset = sales_orders_queryset()
    serializer_class = SalesOrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ('customer__company_name', 'id')
    ordering_fields = ('created_at', 'total_amount', 'status')


class PaymentTransactionViewSet(viewsets.ModelViewSet):
    """CRUD completo de transacoes de pagamento."""

    queryset = payments_queryset()
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
