import tensorflow as tf
from tensorflow.keras import layers, models, datasets

(x_train, y_train), (x_test, y_test) = datasets.cifar10.load_data()
x_train = tf.image.resize(x_train, (96, 96)) / 255.0
x_test = tf.image.resize(x_test, (96, 96)) / 255.0

base = tf.keras.applications.MobileNetV2(
    include_top=False,
    input_shape=(96, 96, 3),
    pooling='avg',
    weights='imagenet'
)
base.trainable = False

model = models.Sequential([
    base,
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=3, batch_size=64,
          validation_split=0.1, verbose=2)

print("Eval:", model.evaluate(x_test, y_test, verbose=2))
