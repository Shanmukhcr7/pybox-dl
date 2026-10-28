import tensorflow as tf
from tensorflow.keras import layers, models, datasets, preprocessing

max_features = 10000
maxlen = 200

(x_train, y_train), (x_test, y_test) = datasets.imdb.load_data(
    num_words=max_features
)

x_train = preprocessing.sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = preprocessing.sequence.pad_sequences(x_test, maxlen=maxlen)

model = models.Sequential([
    layers.Embedding(max_features, 128),
    layers.LSTM(64),
    layers.Dense(1, activation="sigmoid")
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.fit(
    x_train, y_train,
    epochs=3,
    batch_size=64,
    validation_split=0.2,
    verbose=2
)

print("Test:", model.evaluate(x_test, y_test, verbose=2))
