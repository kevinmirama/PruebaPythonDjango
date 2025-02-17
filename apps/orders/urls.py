# apps/orders/urls.py
from django.urls import path
from .views import route_index, get_orders_woocommerce, get_local_orders

urlpatterns = [
    path('', route_index, name='route_index'),
    path('woocommerce/', get_orders_woocommerce, name='get_orders_woocommerce'),
    path('local/', get_local_orders, name='get_local_orders'),
]

