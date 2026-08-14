import torchtext
from torchtext.data.utils import get_tokenizer

# Test the Regex Tokenizer (hits regex.cpp)
print("Testing tokenizer...")
tokenizer = get_tokenizer("basic_english")
tokens = tokenizer("Hello world! Torchtext is finally building on Python 3.14.")
print(f"Tokens: {tokens}\n")

# Test the Vocab Builder (hits vocab.cpp)
print("Testing vocab builder...")
from torchtext.vocab import build_vocab_from_iterator
vocab = build_vocab_from_iterator([tokens])
print(f"Vocab mapping: {vocab.get_stoi()}")
