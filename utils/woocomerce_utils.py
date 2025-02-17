# utils/woocommerce_utils.py
from utils.make_woocommerce_request import make_woocommerce_request

def update_product_in_woocommerce(product):
    """
    Actualiza un producto en WooCommerce mediante su API.
    
    Args:
        product (Product): El objeto Product de Django que se va a actualizar.
    """
    if not product.external_id:
        print(f"El producto {product.id} no tiene external_id. No se puede actualizar en WooCommerce.")
        return

    endpoint = f"products/{product.external_id}"  # Endpoint para actualizar un producto en WooCommerce
    data = {
        "name": product.name,
        "price": str(product.price),
        "stock_quantity": product.inventory,
        "description": product.description
    }
    
    try:
        response = make_woocommerce_request(endpoint, method="PUT", data=data)
        if response.status_code == 200:
            print(f"Producto {product.external_id} actualizado en WooCommerce")
            print("Aqui va la respuesta")
            print(response.text)
        else:
            print(f"Error al actualizar el producto {product.external_id} en WooCommerce: {response.status_code}")
            print(f"Respuesta de la API: {response.text}")  # Mostrar la respuesta de la API para depuración
    except Exception as e:
        print(f"Error en la solicitud a WooCommerce: {str(e)}")