from network_lib.functions import network_functions as fnf
from network_lib.functions.math_functions import convert_truths_to_integer
from network_lib.functions import model_definition as modeldef
from network_lib.functions import ui_functions as fui

def train_network(data_path):
    # Load the data and preprocess it
    # (Assuming your data is stored in a NumPy array called `data` with shape (num_samples, 64, 64, 125) and a NumPy array called `truths` with shape (num_samples, 3))
    data, truths = fnf.load_tiff_data(data_path)

    # Scales data to 0-1 for network input
    data = data.astype('float32') / 255

    #randomly crops images down to 32x32x125
    #print(data.shape)
    #data, truths = util.random_crop(data, truths)
    #print(data.shape)

    # Augments data throught the utility function
    data, truths = fnf.augment_data(data, truths)

    # Define the model
    model = modeldef.define_model()

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    test_accuracy = 0
    while(test_accuracy < 0.6):
        print("\n-----------------------------\nRunning training")
        # Randomizing order of the data
        loop_data, loop_truths = fnf.randomize_data(data, truths)

        # Splits n number of images off from the dataset to be used as test data after training
        n = 100
        loop_data_test, loop_truths_test, loop_data, loop_truths = fnf.extract_and_return_remaining_data(loop_data, loop_truths, n)
        
        # Train the model
        model.fit(loop_data, loop_truths, batch_size=32, epochs=5)

        # Evaluate the model on the test data
        test_loss, test_accuracy = model.evaluate(loop_data_test, loop_truths_test, batch_size=32)
        print("-----------------------------")
        print('Training dataset size:', len(loop_data))
        print('Test dataset size:', len(loop_data_test))
        print('Test loss:', test_loss)
        print('Test accuracy:', test_accuracy)

    fui.ask_to_save_model(model)

def run_model_test(model_path, data_path):
    #load model in from saved model file
    model = fnf.load_model(model_path)

    #load data in from file
    data, truths = fnf.load_tiff_data(data_path)

    # Scales data to 0-1 for network input
    data = data.astype('float32') / 255

    # Augments data throught the utility function
    data, truths = fnf.augment_data(data, truths)

    # Randomizing order of the data
    data, truths = fnf.randomize_data(data, truths)

    # Splits n number of images off from the dataset to be used as test data after training
    n = 20**2
    data_test, truths_test, _, _ = fnf.extract_and_return_remaining_data(data, truths, n)

    predicted_truths = fnf.predict_class(model, data_test)

    truths_test = convert_truths_to_integer(truths_test)

    fui.plot_outputs(truths_test, predicted_truths)

def predict(filepath, modelpath):
    image = fnf.load_single_tiff(filepath)
    model = fnf.load_model(modelpath)
    return fnf.predict_class(model, image)