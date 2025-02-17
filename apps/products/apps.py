# apps/products/apps.py
from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.products'

    def ready(self):
        """
        Método que se ejecuta cuando la aplicación está lista.
        Aquí registramos las señales.
        """
        # Importar y registrar las señales
        import apps.products.signals



