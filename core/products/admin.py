"""Configuracao do Django admin para catalogo e fornecedores."""

from django.contrib import admin

from products.models import Category, Product, Supplier


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Apresentacao das categorias no painel administrativo."""

    list_display = ('name', 'slug', 'is_featured', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """Apresentacao dos fornecedores no painel administrativo."""

    list_display = ('name', 'email', 'phone', 'lead_time_days', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'email')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Apresentacao dos produtos no painel administrativo."""

    list_display = ('name', 'sku', 'category', 'supplier', 'price', 'stock', 'status')
    list_filter = ('status', 'category', 'supplier')
    search_fields = ('name', 'sku')
