import utility as util
import model as modeldef

def train_network():
    # Load the data and preprocess it
    # (Assuming your data is stored in a NumPy array called `data` with shape (num_samples, 64, 64, 125) and a NumPy array called `truths` with shape (num_samples, 3))
    data, truths = util.load_tiff_data("C:\\Users\\binar\\Documents\\Workshop\\School\\ENG4000\\NewNetwork\\data")

    # Scales data to 0-1 for network input
    data = data.astype('float32') / 255

    #randomly crops images down to 32x32x125
    #print(data.shape)
    #data, truths = util.random_crop(data, truths)
    #print(data.shape)

    # Augments data throught the utility function
    data, truths = util.augment_data(data, truths)

    # Randomizing order of the data
    data, truths = util.randomize_data(data, truths)

    # Splits n number of images off from the dataset to be used as test data after training
    n = 100
    data_test, truths_test, data, truths = util.extract_and_return_remaining_data(data, truths, n)

    # Define the model
    model = modeldef.define_model()

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(data, truths, batch_size=32, epochs=5)

    # Evaluate the model on the test data
    test_loss, test_accuracy = model.evaluate(data_test, truths_test, batch_size=32)
    print("-----------------------------")
    print('Training dataset size:', len(data))
    print('Test dataset size:', len(data_test))
    print("-----------------------------")
    print('Test loss:', test_loss)
    print('Test accuracy:', test_accuracy)

    util.ask_to_save_model(model)

def run_model():
    #load model in from saved model file
    model = util.load_model("C:\\Users\\binar\\Documents\\Workshop\\School\\ENG4000\\ENG4KP11\\saved_models\\trained_model_2023-02-03_14-59-39.h5")

    #load data in from file
    data, truths = util.load_tiff_data("C:\\Users\\binar\\Documents\\Workshop\\School\\ENG4000\\NewNetwork\\data")

    # Scales data to 0-1 for network input
    data = data.astype('float32') / 255

    # Augments data throught the utility function
    data, truths = util.augment_data(data, truths)

    # Randomizing order of the data
    data, truths = util.randomize_data(data, truths)

    # Splits n number of images off from the dataset to be used as test data after training
    n = 20**2
    data_test, truths_test, _, _ = util.extract_and_return_remaining_data(data, truths, n)
    
    print(data_test.shape)

    predicted_truths = util.predict_class(model, data_test)

    truths_test = util.convert_truths_to_integer(truths_test)

    util.plot_prediction_grid(truths_test, predicted_truths)