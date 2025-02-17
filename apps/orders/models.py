# apps/orders/models.py
from django.db import models
from apps.clients.models import ClientModel, AddressModel
from apps.products.models import Product

class OrderModel(models.Model):
    client = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(AddressModel, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)
    external_id = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField(null=True, blank=True)  # Hacemos el campo opcional

    def __str__(self):
        return f"Order {self.id} - {self.client.nombre}"

class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"