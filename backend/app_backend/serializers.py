from django.db import transaction, models
from rest_framework import serializers
from .models import Account, Inventory, Maintenance, Order, Product
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Account(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
    def create(self, validated_data):
        items = validated_data.get('items', [])
        with transaction.atomic():
            # 1. Validate stock BEFORE creating the order
            for item in items:
                product_id = item.get('productId') or item.get('ids')
                qty = int(item.get('quantity', 0))
                try:
                    product = Product.objects.select_for_update().get(pk=product_id)
                except Product.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Product {product_id} does not exist."
                    )
                if product.stock < qty:
                    raise serializers.ValidationError(
                        f"Not enough stock for {product.name}. "
                        f"Available: {product.stock}, requested: {qty}."
                    )
            # 2. Create the order
            order = Order.objects.create(**validated_data)
            # 3. Deduct stock atomically
            for item in items:
                product_id = item.get('productId') or item.get('id')
                qty = int(item.get('quantity', 0))
                Product.objects.filter(pk=product_id).update(
                    stock=models.F('stock') - qty
                )
            # 4. Tally liters for maintenance tracking
            import re
            total_liters = 0
            for item in items:
                name = item.get('name', '')
                match = re.search(r'(\d+)\s*(?:Liter|L)', name, re.IGNORECASE)
                liters_per_unit = int(match.group(1)) if match else 0
                total_liters += liters_per_unit * int(item.get('quantity', 0))
            if total_liters:
                maintenance = Maintenance.objects.first()
                if maintenance:
                    Maintenance.objects.filter(pk=maintenance.pk).update(
                        liters_since_last_service=models.F('liters_since_last_service') + total_liters
                    )
            # 5. Broadcast update to dashboard, and to all WEbSocket clients

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'dashboard',
                {
                    'type': 'dashboard.update',
                    'data': {
                        'event': 'new_order',
                        'order_id': str(order.id),
                        'total_amount': str(order.totalAmount),
                    }
                }
            )
        return order
    
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'