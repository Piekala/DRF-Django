"""Serializers da API de clientes."""

from rest_framework import serializers

from customers.models import Customer, CustomerAddress, CustomerSegment
from customers.services import ensure_single_main_address


class CustomerSegmentSerializer(serializers.ModelSerializer):
    """Serializa segmentos de clientes."""

    class Meta:
        model = CustomerSegment
        fields = ('id', 'name', 'description', 'created_at', 'updated_at')


class CustomerAddressSerializer(serializers.ModelSerializer):
    """Serializa enderecos e aplica a regra de endereco principal unico."""

    class Meta:
        model = CustomerAddress
        fields = (
            'id',
            'customer',
            'label',
            'street',
            'city',
            'state',
            'postal_code',
            'is_main',
            'created_at',
            'updated_at',
        )

    def create(self, validated_data):
        """Cria o endereco e ajusta a consistencia do principal antes de salvar."""
        if validated_data.get('is_main'):
            CustomerAddress.objects.filter(customer=validated_data['customer'], is_main=True).update(is_main=False)
        address = super().create(validated_data)
        return address

    def update(self, instance, validated_data):
        """Atualiza o endereco e reaplica a regra de principal unico."""
        if validated_data.get('is_main'):
            CustomerAddress.objects.filter(customer=instance.customer, is_main=True).exclude(pk=instance.pk).update(is_main=False)
        address = super().update(instance, validated_data)
        return address


class CustomerSerializer(serializers.ModelSerializer):
    """Serializa clientes incluindo os enderecos somente para leitura."""

    addresses = CustomerAddressSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = (
            'id',
            'segment',
            'account_manager',
            'company_name',
            'document',
            'email',
            'phone',
            'status',
            'credit_limit',
            'notes',
            'addresses',
            'created_at',
            'updated_at',
        )
