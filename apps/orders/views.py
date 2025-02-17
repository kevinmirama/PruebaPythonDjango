from rest_framework.response import Response
from rest_framework.decorators import api_view
from utils.make_woocommerce_request import make_woocommerce_request
from .models import OrderModel, OrderItemModel
from apps.clients.models import ClientModel, AddressModel
from apps.products.models import Product
from .serializers import OrderModelSerializer
from decimal import Decimal

@api_view(["GET"])
def route_index(request):
    return Response({
        "message": "Bienvenido a la API de órdenes",
        "endpoints": {
            "orders_woocommerce": "/woocommerce/",
            "local_orders": "/local/"
        }
    })

@api_view(["GET"])
def get_orders_woocommerce(request):
    try:
        response = make_woocommerce_request("orders", method="GET")
        orders_data = response.json()

        orders_created = 0
        orders_skipped = 0

        for order_data in orders_data:
            try:
                # Crear o actualizar el cliente
                client, _ = ClientModel.objects.get_or_create(
                    id=order_data["customer_id"],
                    defaults={
                        "name": f"{order_data['billing']['first_name']} {order_data['billing']['last_name']}",
                        "email": order_data["billing"]["email"],
                    }
                )

                # Crear o actualizar la dirección
                address, _ = AddressModel.objects.get_or_create(
                    client=client,
                    defaults={
                        "address": order_data["billing"]["address_1"],
                        "city": order_data["billing"]["city"],
                        "state": order_data["billing"]["state"],
                        "country": order_data["billing"]["country"],
                    }
                )

                # Crear o actualizar la orden
                order, created = OrderModel.objects.get_or_create(
                    external_id=str(order_data["id"]),
                    defaults={
                        "client": client,
                        "address": address,
                        "total": Decimal(order_data["total"]),
                        "fecha": order_data["date_created"],
                        "status": order_data["status"]
                    }
                )

                if not created:
                    orders_skipped += 1
                    continue

                orders_created += 1

                # Procesar items de la orden
                for item_data in order_data["line_items"]:
                    product, _ = Product.objects.get_or_create(
                        external_id=str(item_data["product_id"]),
                        defaults={
                            "name": item_data["name"],
                            "price": Decimal(item_data["price"]),
                            "inventory": item_data.get("quantity", 0),
                            "description": item_data.get("description", "")
                        }
                    )

                    OrderItemModel.objects.create(
                        order=order,
                        product=product,
                        quantity=item_data["quantity"],
                        unit_price=Decimal(item_data["price"])
                    )

            except Exception as e:
                print(f"Error processing order {order_data.get('id')}: {str(e)}")
                continue

        return Response({
            "message": "Proceso completado",
            "orders_created": orders_created,
            "orders_skipped": orders_skipped
        })

    except Exception as e:
        return Response({
            "error": f"Error al procesar órdenes de WooCommerce: {str(e)}"
        }, status=500)

@api_view(["GET"])
def get_local_orders(request):
    ordenes = OrderModel.objects.all()
    serializer = OrderModelSerializer(ordenes, many=True)
    return Response(serializer.data)