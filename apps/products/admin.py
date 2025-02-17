# apps/products/admin.py
from django.contrib import admin
from .models import Product  # Importa el modelo Product

# Registra el modelo Product en el admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'inventory', 'external_id')  # Campos que se mostrarán en la lista
    search_fields = ('name', 'external_id')  # Campos por los que se puede buscar
    list_filter = ('price', 'inventory')  # Filtros laterales
