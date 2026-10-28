# Week 6: Implement Language Modeling using RNN

import numpy as np
from tensorflow.keras import layers, models, utils

text = "hello world this is a long toy dataset for class level language modeling"

chars = sorted(list(set(text)))
char2idx = {c: i for i, c in enumerate(chars)}
idx2char = {i: c for c, i in char2idx.items()}
vocab_size = len(chars)
seq_length = 20

sentences = []
next_chars = []
for i in range(len(text) - seq_length):
    sentences.append(text[i:i + seq_length])
    next_chars.append(text[i + seq_length])

X = np.zeros((len(sentences), seq_length, vocab_size), dtype=bool)
y = np.zeros((len(sentences), vocab_size), dtype=bool)

for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char2idx[char]] = 1
    y[i, char2idx[next_chars[i]]] = 1

model = models.Sequential([
    layers.Input(shape=(seq_length, vocab_size)),
    layers.LSTM(128),
    layers.Dense(vocab_size, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy"
)

model.fit(X, y, batch_size=32, epochs=100, verbose=0)
print("Trained small char-RNN (toy)")

seed = sentences[0]
print("Seed:", seed)

for _ in range(100):
    x_pred = np.zeros((1, seq_length, vocab_size))
    for t, char in enumerate(seed):
        x_pred[0, t, char2idx[char]] = 1
    preds = model.predict(x_pred, verbose=0)[0]
    next_char = idx2char[np.argmax(preds)]
    seed = seed[1:] + next_char

print("Generated tail:", seed)
