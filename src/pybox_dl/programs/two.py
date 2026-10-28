# Week 2: Implementation of Package TensorFlow

import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

x = np.random.random((1000, 20))
y = np.random.randint(0, 10, size=(1000,))

model = models.Sequential([
    layers.Input(shape=(20,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(x, y, epochs=5, batch_size=32, verbose=2)
print("Final accuracy:", history.history['accuracy'][-1])
