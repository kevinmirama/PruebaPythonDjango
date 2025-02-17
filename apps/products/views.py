# apps/products/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from utils.make_woocommerce_request import make_woocommerce_request

@api_view(['PUT'])
def edit_product(request, product_id):
    """
    Edit a product both in Django database and WooCommerce
    """
    product = get_object_or_404(Product, id=product_id)
    data = request.data

    # Preparar datos para WooCommerce
    woo_data = {
        'name': data.get('name', product.name),
        'regular_price': str(data.get('price', product.price)),
        'stock_quantity': data.get('inventory', product.inventory),
        'description': data.get('description', product.description),
    }

    # Si el producto tiene external_id, actualizarlo en WooCommerce
    if product.external_id:
        try:
            # Actualizar en WooCommerce
            woo_response = make_woocommerce_request(
                f'products/{product.external_id}',
                'PUT',
                woo_data
            )
            
            if not isinstance(woo_response, dict):
                return Response({
                    'error': 'Failed to update product in WooCommerce'
                }, status=400)

        except Exception as e:
            return Response({
                'error': f'Error updating product in WooCommerce: {str(e)}'
            }, status=400)
    
    # Actualizar en la base de datos local
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.inventory = data.get('inventory', product.inventory)
    product.description = data.get('description', product.description)
    product.save()

    return Response({
        'message': 'Product updated successfully',
        'product': {
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'inventory': product.inventory,
            'description': product.description,
            'external_id': product.external_id
        }
    })

# Función auxiliar para crear productos en WooCommerce
def create_product_in_woocommerce(product):
    
    woo_data = {
        'name': product.name,
        'regular_price': str(product.price),
        'stock_quantity': product.inventory,
        'description': product.description,
    }

    try:
        woo_response = make_woocommerce_request('products', 'POST', woo_data)
        if isinstance(woo_response, dict) and 'id' in woo_response:
            product.external_id = str(woo_response['id'])
            product.save()
            return True
    except Exception:
        pass
    return False