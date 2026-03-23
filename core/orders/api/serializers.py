"""Serializers da API de pedidos."""

from rest_framework import serializers

from orders.models import PaymentTransaction, SalesOrder, SalesOrderItem
from orders.services import create_order, update_order


class SalesOrderItemSerializer(serializers.ModelSerializer):
    """Serializa os itens do pedido, incluindo o nome do produto para leitura."""

    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = SalesOrderItem
        fields = ('id', 'product', 'product_name', 'quantity', 'unit_price', 'line_total')
        read_only_fields = ('line_total',)

    def validate(self, attrs):
        """Impede preco manual diferente do catalogo do produto."""
        product = attrs['product']
        unit_price = attrs.get('unit_price')
        if unit_price is not None and unit_price != product.price:
            raise serializers.ValidationError(
                {'unit_price': 'O preco do item deve ser definido pelo catalogo do produto.'}
            )
        return attrs


class PaymentTransactionSerializer(serializers.ModelSerializer):
    """Serializa transacoes de pagamento."""

    class Meta:
        model = PaymentTransaction
        fields = (
            'id',
            'order',
            'provider',
            'external_id',
            'amount',
            'status',
            'paid_at',
            'created_at',
            'updated_at',
        )


class SalesOrderSerializer(serializers.ModelSerializer):
    """Serializa o pedido principal junto com seus itens."""

    items = SalesOrderItemSerializer(many=True)
    customer_name = serializers.CharField(source='customer.company_name', read_only=True)

    class Meta:
        model = SalesOrder
        fields = (
            'id',
            'customer',
            'customer_name',
            'salesperson',
            'status',
            'expected_delivery',
            'notes',
            'subtotal',
            'shipping_fee',
            'discount_amount',
            'total_amount',
            'items',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('subtotal', 'total_amount')

    def validate_items(self, value):
        """Exige pelo menos um item para manter o pedido util."""
        if not value:
            raise serializers.ValidationError('Informe pelo menos um item.')
        return value

    def create(self, validated_data):
        """Delegacao para a camada de servico, onde esta a regra principal."""
        items_data = validated_data.pop('items')
        return create_order(order_data=validated_data, items_data=items_data)

    def update(self, instance, validated_data):
        """Delegacao para a camada de servico ao atualizar o pedido."""
        items_data = validated_data.pop('items', None)
        return update_order(instance=instance, order_data=validated_data, items_data=items_data)
