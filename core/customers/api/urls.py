"""Rotas REST do modulo de clientes."""

from rest_framework.routers import DefaultRouter

from customers.api.views import CustomerAddressViewSet, CustomerSegmentViewSet, CustomerViewSet

router = DefaultRouter()
router.register('segments', CustomerSegmentViewSet, basename='customer-segment')
router.register('customers', CustomerViewSet, basename='customer')
router.register('addresses', CustomerAddressViewSet, basename='customer-address')

urlpatterns = router.urls
