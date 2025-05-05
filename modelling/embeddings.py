from pinecone import Pinecone, ServerlessSpec
import os 
from langchain.embeddings import OllamaEmbeddings
from .load_transformer import embed_text
from products.models import Product
pc = Pinecone(api_key=os.environ.get('pinacone_key'))

index = "product-index"

index_connect = pc.Index(index)



def prepare_text(product):
    return f"name:{product.name}.color:{product.color}.price:{product.price}"



def push_into_pinacone():
    product = Product.objects.all()
    vectors = []

    for p in product:
        data = prepare_text(p)
        vector = embed_text(data)
        vectors.append((str(p.pk),vector[0][0]))
        print(vectors)
    if not vectors:
        print("Empty embeddings")
    else:
        index_connect.upsert(vectors=vectors)



