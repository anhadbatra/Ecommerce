from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver

PRODUCT_DATA_FILE = "product_data.txt"

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        from products.models import Product  # Import inside ready() to avoid circular import

        def export_product_data(**kwargs):
            products = Product.objects.all()
            print(products)
            product_data = "\n".join(
                f"PK: {p.pk}, Name: {p.name}, Price: {p.price}"
                for p in products
            )
            with open(PRODUCT_DATA_FILE, 'w') as f:
                f.write(product_data)

        post_migrate.connect(export_product_data, sender=self)
