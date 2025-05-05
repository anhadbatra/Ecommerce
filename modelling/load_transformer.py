from .train import Simple_Transformer
import os
import torch

vocab = {"<PAD>": 0, "<EOS>": 1, "find": 2, "products": 3, "price": 4, "high": 5, 
         "between": 6, "less": 7, "[": 8, "]": 9, "1": 10, "2": 11, "3": 12}

model = Simple_Transformer(
    vocab_size=len(vocab),
    d_model = 768,
    n_heads=4,
    n_layers = 2,
    d_ff = 512,
    max_seq_length=20
)
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'embeddings.pth')
model.load_state_dict(torch.load(model_path))
model.eval()
def embed_text(text):
    with torch.no_grad():
        encoded = model.encode_text(text,model,vocab)
        return encoded