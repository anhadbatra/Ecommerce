from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        from modelling.embeddings import push_into_pinacone
        from modelling.train import Simple_Transformer
        model = Simple_Transformer()
        vocab = {"<PAD>": 0, "<EOS>": 1, "find": 2, "products": 3, "price": 4, "high": 5, 
         "between": 6, "less": 7, "[": 8, "]": 9, "1": 10, "2": 11, "3": 12}
        vocab_size = len(vocab)
        word_to_idx = vocab
        idx_to_word = {v: k for k, v in vocab.items()}

        train_examples = [
        ([2, 3], [8, 10, 9]), 
        ([2, 4], [8, 11, 9]),  
        ([2, 5], [8, 12, 9]),
    ]
        model.__init__()



