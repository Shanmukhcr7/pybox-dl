import tensorflow as tf
from tensorflow.keras import layers, models


x = tf.random.uniform((200, 128, 128, 3))
y = tf.random.uniform((200,), maxval=5, dtype=tf.int32)

model = models.Sequential([
    layers.Input(shape=(128, 128, 3)),
    layers.Conv2D(32, 3, activation='relu'),
    layers.MaxPool2D(),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPool2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(5, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x, y, epochs=8, batch_size=16, verbose=2)
