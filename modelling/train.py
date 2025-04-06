import torch
import torch.nn as nn
import math

class Simple_Transformer(nn.Module):
    def __init__(self, vocab_size, d_model, n_heads, n_layers, d_ff, max_seq_length, dropout=0.1):
        super(Simple_Transformer, self).__init__()
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = self.create_positional_encoding(max_seq_length, d_model)
        self.decoder_layers = nn.ModuleList([
            nn.TransformerDecoderLayer(d_model, n_heads, d_ff, dropout)
            for _ in range(n_layers)
        ])
        self.fc_out = nn.Linear(d_model, vocab_size)
        self.dropout = nn.Dropout(dropout)
        self.scale = math.sqrt(d_model)
    

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
