import numpy as np
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from utility import *

tf.data.experimental.enable_debug_mode()

# Load the data and preprocess it
# (Assuming your data is stored in a NumPy array called `X` with shape (num_samples, 64, 64, 125) and a NumPy array called `y` with shape (num_samples, 3))
X, y = load_tiff_data("C:\\Users\\binar\\Documents\\Workshop\\School\\ENG4000\\NewNetwork\\data")

X, y = augment_data(X, y)

X_test, y_test, X, y = extract_and_return_remaining_data(X, y, 100)

X = X.astype('float32') / 255

# Define the model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 125)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(3, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'], run_eagerly=True)

# Train the model
model.fit(X, y, batch_size=32, epochs=5)

# Evaluate the model on the test data
test_loss, test_accuracy = model.evaluate(X_test, y_test, batch_size=32)
print("-----------------------------")
print('Training dataset size:', len(X))
print('Test dataset size:', len(X_test))
print("-----------------------------")
print('Test loss:', test_loss)
print('Test accuracy:', test_accuracy)