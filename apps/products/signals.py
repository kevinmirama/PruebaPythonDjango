# apps/products/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from utils.woocomerce_utils import update_product_in_woocommerce

@receiver(post_save, sender=Product)
def sync_product_with_woocommerce(sender, instance, **kwargs):
    """
    Sincroniza un producto con WooCommerce cuando se guarda en Django.
    """
    print(f"Señal post_save detectada para el producto {instance.id}")  # Log para verificar que la señal se ejecuta
    if instance.external_id:  # Solo sincronizar si el producto ya existe en WooCommerce
        update_product_in_woocommerce(instance)