# apps/orders/serializers.py
from rest_framework import serializers
from .models import OrderModel, OrderItemModel
from apps.clients.models import ClientModel, AddressModel

class AddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = '__all__'

class ClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields = '__all__'

class OrderItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemModel
        fields = ['id', 'product', 'quantity', 'unit_price']

class OrderModelSerializer(serializers.ModelSerializer):
    client = ClientModelSerializer()
    address = AddressModelSerializer()
    items = OrderItemModelSerializer(many=True)

    class Meta:
        model = OrderModel
        fields = ['id', 'client', 'address', 'total', 'created_at', 
                 'status', 'external_id', 'fecha', 'items']