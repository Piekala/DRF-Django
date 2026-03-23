"""Configuracao do Django admin para logistica."""

from django.contrib import admin

from shipping.models import Shipment, ShipmentItem, Warehouse


class ShipmentItemInline(admin.TabularInline):
    """Permite visualizar itens enviados dentro da remessa."""

    model = ShipmentItem
    extra = 1


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    """Apresentacao dos armazens no painel administrativo."""

    list_display = ('name', 'code', 'city', 'state', 'is_active')
    list_filter = ('is_active', 'state')
    search_fields = ('name', 'code')


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    """Apresentacao das remessas no painel administrativo."""

    list_display = ('tracking_code', 'order', 'warehouse', 'carrier', 'status', 'created_at')
    list_filter = ('status', 'carrier', 'warehouse')
    search_fields = ('tracking_code', 'order__id')
    inlines = [ShipmentItemInline]
