"""Configuracao do Django admin para clientes."""

from django.contrib import admin

from customers.models import Customer, CustomerAddress, CustomerSegment


@admin.register(CustomerSegment)
class CustomerSegmentAdmin(admin.ModelAdmin):
    """Apresentacao dos segmentos no painel administrativo."""

    list_display = ('name', 'created_at')
    search_fields = ('name',)


class CustomerAddressInline(admin.TabularInline):
    """Permite editar enderecos diretamente dentro do cliente."""

    model = CustomerAddress
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Apresentacao dos clientes no painel administrativo."""

    list_display = ('company_name', 'document', 'status', 'segment', 'account_manager')
    list_filter = ('status', 'segment')
    search_fields = ('company_name', 'document', 'email')
    inlines = [CustomerAddressInline]
