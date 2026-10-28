# Week 3: Implementation of Neural Network
# Aim: Program to implement an Artificial Neural Network (ANN)
# for classification using Python.

# keras_mnist_mlp.py
import tensorflow as tf
from tensorflow.keras import layers, models, datasets

(x_train, y_train), (x_test, y_test) = datasets.mnist.load_data()

x_train = x_train.reshape(-1, 28 * 28).astype('float32') / 255.
x_test = x_test.reshape(-1, 28 * 28).astype('float32') / 255.

model = models.Sequential([
    layers.Input(shape=(28 * 28,)),
    layers.Dense(256, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5, batch_size=128,
          validation_split=0.1, verbose=2)

print("Test eval:", model.evaluate(x_test, y_test, verbose=2))
