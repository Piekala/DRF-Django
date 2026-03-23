"""Rotas REST do modulo de logistica."""

from rest_framework.routers import DefaultRouter

from shipping.api.views import ShipmentViewSet, WarehouseViewSet

router = DefaultRouter()
router.register('warehouses', WarehouseViewSet, basename='warehouse')
router.register('shipments', ShipmentViewSet, basename='shipment')

urlpatterns = router.urls
