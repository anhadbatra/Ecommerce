from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        from modelling.embeddings import push_into_pinacone
        from modelling.train import Simple_Transformer
        push_into_pinacone()



