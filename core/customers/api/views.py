"""Views DRF do modulo de clientes."""

from rest_framework import permissions, viewsets

from customers.api.serializers import CustomerAddressSerializer, CustomerSegmentSerializer, CustomerSerializer
from customers.selectors import customer_addresses_queryset, customer_segments_queryset, customers_queryset


class CustomerSegmentViewSet(viewsets.ModelViewSet):
    """CRUD completo de segmentos de clientes."""

    queryset = customer_segments_queryset()
    serializer_class = CustomerSegmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ('name',)


class CustomerViewSet(viewsets.ModelViewSet):
    """CRUD completo de clientes corporativos."""

    queryset = customers_queryset()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ('company_name', 'document', 'email')
    ordering_fields = ('company_name', 'created_at', 'credit_limit')


class CustomerAddressViewSet(viewsets.ModelViewSet):
    """CRUD completo de enderecos de clientes."""

    queryset = customer_addresses_queryset()
    serializer_class = CustomerAddressSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
