from django.apps import AppConfig

PRODUCT_DATA_FILE = "product_data.txt"

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    #def ready(self):
        #from .models import Product
       # products = Product.objects.all()
        #product_data = "\n".join(
        #f"PK: {p.pk}, Name: {p.name}, Price: {p.price}"
        #for p in products
    #)
     #   with open(PRODUCT_DATA_FILE, 'w') as f:
      #      f.write(product_data)
