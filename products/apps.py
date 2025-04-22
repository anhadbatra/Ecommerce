from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver

PRODUCT_DATA_FILE = "product_data.txt"

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        from modelling.embeddings import push_into_pinacone
        push_into_pinacone()


