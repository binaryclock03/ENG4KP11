from utility import *
from model import *

# Load the data and preprocess it
# (Assuming your data is stored in a NumPy array called `X` with shape (num_samples, 64, 64, 125) and a NumPy array called `y` with shape (num_samples, 3))
X, y = load_tiff_data("C:\\Users\\binar\\Documents\\Workshop\\School\\ENG4000\\NewNetwork\\data")

# augments data throught the utility function
X, y = augment_data(X, y)

# Scales data to 0-1 for network input
X = X.astype('float32') / 255

# Splits n number of images off from the dataset to be used as test data after training
n = 100
X_test, y_test, X, y = extract_and_return_remaining_data(X, y, n)

# Define the model
model = define_model()

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

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