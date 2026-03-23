"""Rotas REST do modulo de pedidos."""

from rest_framework.routers import DefaultRouter

from orders.api.views import PaymentTransactionViewSet, SalesOrderViewSet

router = DefaultRouter()
router.register('orders', SalesOrderViewSet, basename='sales-order')
router.register('payments', PaymentTransactionViewSet, basename='payment')

urlpatterns = router.urls
