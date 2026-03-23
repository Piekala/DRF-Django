"""Roteador principal do projeto, delegando rotas para cada modulo."""

from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Marketplace B2B API',
        default_version='v1',
        description='Documentação Swagger para a API do marketplace',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='devops@example.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.api.urls')),
    path('api/v1/products/', include('products.api.urls')),
    path('api/v1/customers/', include('customers.api.urls')),
    path('api/v1/orders/', include('orders.api.urls')),
    path('api/v1/shipping/', include('shipping.api.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
