import torch
import torch.nn as nn
import math



class Simple_Transformer(nn.Module):

    def __init__(self, vocab_size, d_model, n_heads, n_layers, d_ff, max_seq_length, dropout=0.1):
        super(Simple_Transformer, self).__init__()
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = self.position_encoding(max_seq_length, d_model)
        self.decoder_layers = nn.ModuleList([
            nn.TransformerDecoderLayer(d_model, n_heads, d_ff, dropout)
            for _ in range(n_layers)
        ])
        self.fc_out = nn.Linear(d_model, vocab_size)
        self.dropout = nn.Dropout(dropout)
        self.scale = math.sqrt(d_model)
        
    
    def position_encoding(self,max_len,d_model):
        positional_matrix = torch.zeros(max_len,d_model)
        for pos in range(max_len):
            for i in range(0,d_model,2):
                angle = pos / (10000 ** ((2 * i) / d_model))
                positional_matrix[pos,i] = math.sin(angle)
                if i + 1 < d_model:
                    positional_matrix[pos,i+1] = math.cos(angle)
        return positional_matrix
    @staticmethod   
    def tokenize(text, word_to_idx, max_len=10):
        tokens = [word_to_idx.get(word.lower(), word_to_idx["<PAD>"]) for word in text.split()]
        tokens = tokens[:max_len]
        while len(tokens) < max_len:
            tokens.append(word_to_idx["<PAD>"])
        return torch.tensor(tokens).unsqueeze(0) 
    @staticmethod
    def encode_text(text, model, word_to_idx):
        tokenized_text = Simple_Transformer.tokenize(text, word_to_idx)
        with torch.no_grad():
            x = model.embedding(tokenized_text) * model.scale
            pos_en = model.pos_encoding[:x.size(1)].to(x.device)
            x = x + pos_en
        return x 

if __name__ == "__main__":
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
    model = Simple_Transformer(
        vocab_size,
        d_model=128, 
        n_heads=4, 
        n_layers=2, 
        d_ff=512, 
        max_seq_length=20
    )
    tokenzie = model.encode_text("hello",model,word_to_idx)
    print(tokenzie)
    torch.save(model.state_dict(),"embeddings.pth")
