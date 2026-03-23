"""Rotas REST do modulo de produtos."""

from rest_framework.routers import DefaultRouter

from products.api.views import CategoryViewSet, ProductViewSet, SupplierViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('suppliers', SupplierViewSet, basename='supplier')
router.register('products', ProductViewSet, basename='product')

urlpatterns = router.urls
