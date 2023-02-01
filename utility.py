import os
import numpy as np
import imageio
import datetime

## Loading Data
def load_tiff_data(dir_path):
    filenames = [f for f in os.listdir(dir_path) if f.endswith(".tif")]
    num_samples = len(filenames)
    data = np.zeros((num_samples, 64, 64, 125))
    truth = np.zeros((num_samples, 3))
    
    for i, filename in enumerate(filenames):
        image = imageio.imread(os.path.join(dir_path, filename))
        if image.shape[-1] == 126:
            image = image[..., :125]
        data[i, :, :, :] = image
        
        if "Health" in filename:
            truth[i, 0] = 1
        elif "Rust" in filename:
            truth[i, 1] = 1
        else:
            truth[i, 2] = 1
            
    return data, truth

def extract_and_return_remaining_data(data, truth, num_samples):
    indices = np.random.choice(data.shape[0], num_samples, replace=False)
    extracted_data = data[indices]
    extracted_truth = truth[indices]
    remaining_data = np.delete(data, indices, axis=0)
    remaining_truth = np.delete(truth, indices, axis=0)
    return extracted_data, extracted_truth, remaining_data, remaining_truth

def randomize_data(data, truth):
    num_samples = data.shape[0]
    permutation = np.random.permutation(num_samples)
    randomized_data = data[permutation]
    randomized_truth = truth[permutation]
    return randomized_data, randomized_truth

## Augmentation Functions
def augment_data(data, truth):
    data, truth = augment_data_by_flipping_vertically(data, truth)
    data, truth = augment_data_by_rotating(data, truth)
    return data, truth

def augment_data_by_flipping_vertically(data, truth):
    flipped_data = np.flip(data, axis=2)
    augmented_data = np.concatenate((data, flipped_data), axis=0)
    augmented_truth = np.concatenate((truth, truth), axis=0)
    return augmented_data, augmented_truth

def augment_data_by_rotating(data, truth):
    rotated_data = np.rot90(data, k=1, axes=(1, 2))
    augmented_data = np.concatenate((data, rotated_data), axis=0)
    augmented_truth = np.concatenate((truth, truth), axis=0)
    return augmented_data, augmented_truth

## User interaction Functions
def ask_to_save_model(model):
    save = input("Do you want to save the model? (yes/no)")
    if save.lower() == 'yes':
        date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        model.save("saved_models//trained_model_" + date_time + ".h5")
        print("Model saved as 'trained_model_" + date_time + ".h5'")
    else:
        print("Model not saved")