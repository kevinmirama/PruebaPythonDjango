# apps/products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.get_all_products, name='get_all_products'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
]