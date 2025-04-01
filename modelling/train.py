vocab = {"<PAD>": 0, "<EOS>": 1, "find": 2, "products": 3, "price": 4, "high": 5, 
         "between": 6, "less": 7, "[": 8, "]": 9, "1": 10, "2": 11, "3": 12}
vocab_size = len(vocab)
word_to_idx = vocab
idx_to_word = {v: k for k, v in vocab.items()}

train_examples = [
    ([2, 3], [8, 10, 9]),  # "find electronics" -> [1]
    ([2, 4], [8, 11, 9]),  # "find clothing" -> [2]
    ([2, 5], [8, 12, 9]),  # "find furniture" -> [3]
]