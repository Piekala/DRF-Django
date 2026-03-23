"""Serializers da API de logistica."""

from django.db import transaction
from rest_framework import serializers

from shipping.models import Shipment, ShipmentItem, Warehouse
from shipping.services import build_shipment_items


class WarehouseSerializer(serializers.ModelSerializer):
    """Serializa armazens para leitura e escrita na API."""

    class Meta:
        model = Warehouse
        fields = ('id', 'name', 'code', 'city', 'state', 'is_active', 'created_at', 'updated_at')


class ShipmentItemSerializer(serializers.ModelSerializer):
    """Serializa os itens transportados dentro da remessa."""

    class Meta:
        model = ShipmentItem
        fields = ('id', 'order_item', 'quantity')


class ShipmentSerializer(serializers.ModelSerializer):
    """Serializa remessas completas com seus itens."""

    items = ShipmentItemSerializer(many=True)

    class Meta:
        model = Shipment
        fields = (
            'id',
            'order',
            'warehouse',
            'tracking_code',
            'carrier',
            'status',
            'dispatched_at',
            'delivered_at',
            'items',
            'created_at',
            'updated_at',
        )

    def validate(self, attrs):
        """Verifica consistencia entre armazem, pedido e itens enviados."""
        order = attrs['order']
        warehouse = attrs['warehouse']
        items = attrs['items']

        if not warehouse.is_active:
            raise serializers.ValidationError({'warehouse': 'O armazem informado esta inativo.'})

        if order.status == order.Status.CANCELLED:
            raise serializers.ValidationError({'order': 'Nao e possivel criar remessa para pedido cancelado.'})
        if order.status not in {order.Status.PAID, order.Status.CONFIRMED}:
            raise serializers.ValidationError({'order': 'Pedido precisa estar confirmado ou pago para expedir remessa.'})

        for item in items:
            order_item = item['order_item']
            if order_item.order_id != order.id:
                raise serializers.ValidationError(
                    {'items': ['Todos os itens da remessa devem pertencer ao pedido informado.']}
                )
            if item['quantity'] > order_item.quantity:
                raise serializers.ValidationError(
                    {'items': [f'A quantidade enviada para o item {order_item.id} excede o pedido.']}
                )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        """Cria remessa e itens em uma unica transacao atomica."""
        items_data = validated_data.pop('items')
        shipment = Shipment.objects.create(**validated_data)
        build_shipment_items(shipment, items_data)
        return shipment
