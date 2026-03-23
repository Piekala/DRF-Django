"""Configuracao do Django admin para pedidos."""

from django.contrib import admin

from orders.models import PaymentTransaction, SalesOrder, SalesOrderItem


class SalesOrderItemInline(admin.TabularInline):
    """Permite editar itens dentro da tela do pedido."""

    model = SalesOrderItem
    extra = 1


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    """Apresentacao dos pedidos no painel administrativo."""

    list_display = ('id', 'customer', 'status', 'salesperson', 'total_amount', 'created_at')
    list_filter = ('status',)
    search_fields = ('id', 'customer__company_name')
    inlines = [SalesOrderItemInline]


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    """Apresentacao das transacoes de pagamento no admin."""

    list_display = ('order', 'provider', 'amount', 'status', 'paid_at')
    list_filter = ('status', 'provider')
    search_fields = ('external_id', 'order__id')
