"""Serializers da API de produtos."""

from rest_framework import serializers

from products.models import Category, Product, Supplier


class CategorySerializer(serializers.ModelSerializer):
    """Converte categorias entre modelo Python e JSON."""

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'is_featured', 'created_at', 'updated_at')


class SupplierSerializer(serializers.ModelSerializer):
    """Converte fornecedores entre modelo Python e JSON."""

    class Meta:
        model = Supplier
        fields = ('id', 'name', 'email', 'phone', 'lead_time_days', 'is_active', 'created_at', 'updated_at')


class ProductSerializer(serializers.ModelSerializer):
    """Serializa produtos completos, incluindo nomes de relacoes."""

    category_name = serializers.CharField(source='category.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    needs_restock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'category_name',
            'supplier',
            'supplier_name',
            'name',
            'sku',
            'description',
            'price',
            'cost',
            'stock',
            'reorder_level',
            'status',
            'is_published',
            'needs_restock',
            'created_at',
            'updated_at',
        )

    def validate(self, attrs):
        """Impede gravar produto com preco abaixo do custo."""
        price = attrs.get('price', getattr(self.instance, 'price', None))
        cost = attrs.get('cost', getattr(self.instance, 'cost', None))
        if price is not None and cost is not None and price < cost:
            raise serializers.ValidationError({'price': 'O preco de venda nao pode ser menor que o custo.'})
        return attrs


class ProductStockAdjustmentSerializer(serializers.Serializer):
    """Valida o payload enxuto do endpoint de ajuste de estoque."""

    stock = serializers.IntegerField(min_value=0)
