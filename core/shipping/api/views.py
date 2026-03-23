"""Views DRF do modulo de logistica."""

from rest_framework import permissions, viewsets

from shipping.api.serializers import ShipmentSerializer, WarehouseSerializer
from shipping.selectors import shipments_queryset, warehouses_queryset


class WarehouseViewSet(viewsets.ModelViewSet):
    """CRUD completo de armazens."""

    queryset = warehouses_queryset()
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ('name', 'code', 'city')


class ShipmentViewSet(viewsets.ModelViewSet):
    """CRUD completo de remessas."""

    queryset = shipments_queryset()
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ('tracking_code', 'carrier', 'order__id')
