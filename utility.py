import os
from matplotlib.colors import ListedColormap
import numpy as np
import imageio
import datetime
import matplotlib.pyplot as plt
from keras.models import load_model

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

## Loading model
def load_trained_model(model_file_path):
    model = load_model(model_file_path)
    return model

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

""" def random_crop(data, truths, crop_size=(32, 32, 125), overlap=0.25):
    num_samples, h, w, c = data.shape
    crop_h, crop_w, crop_c = crop_size
    assert h >= crop_h and w >= crop_w and c == crop_c, "Crop size should not be larger than the original image size"
    max_overlap_h = int(crop_h * overlap)
    max_overlap_w = int(crop_w * overlap)
    crops = []
    truths_crops = []
    for i in range(num_samples):
        attempts = 0
        while attempts < 5:
            x = np.random.randint(0, h - crop_h + 1)
            y = np.random.randint(0, w - crop_w + 1)
            crop = data[i, x:x+crop_h, y:y+crop_w, :]
            overlap_flag = False
            for prev_crop in crops:
                h_overlap = min(x + crop_h, prev_crop[0] + crop_h) - max(x, prev_crop[0])
                w_overlap = min(y + crop_w, prev_crop[1] + crop_w) - max(y, prev_crop[1])
                if h_overlap > max_overlap_h and w_overlap > max_overlap_w:
                    overlap_flag = True
                    break
            if not overlap_flag:
                crops.append((x, y))
                truths_crops.append(truths[i])
                break
            attempts += 1
    crops = np.stack(crops, axis=0)
    truths_crops = np.stack(truths_crops, axis=0)
    return crops, truths_crops """

## User interaction Functions
def ask_to_save_model(model):
    save = input("Do you want to save the model? [y/n]")
    if save.lower() == 'y':
        date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        model.save("saved_models//trained_model_" + date_time + ".h5")
        print("Model saved as 'trained_model_" + date_time + ".h5'")
    else:
        print("Model not saved")

def plot_outputs(truths, predictions):
    truths = truths.astype(int)
    predictions = predictions.astype(int)

    truth_grid = np.reshape(truths, (int(np.sqrt(truths.shape[0])), -1))
    prediction_grid = np.reshape(predictions, (int(np.sqrt(predictions.shape[0])), -1))
    cmap = ListedColormap(["lawngreen", "red", "grey"])
    fig, ((ax1, ax2, ax5), (ax3, ax4, ax6)) = plt.subplots(2, 3, figsize=(9,6))
    ax1.imshow(truth_grid, cmap= cmap)
    ax1.set_title('Truth')
    ax1.axis('off')
    ax2.imshow(prediction_grid, cmap= cmap)
    ax2.set_title('Prediction')
    ax2.axis('off')

    cmap = ListedColormap(["red", "lawngreen"])
    right_wrong = array_and(truths, predictions)
    right_wrong_grid = np.reshape(right_wrong, (int(np.sqrt(truths.shape[0])), -1))
    ax3.imshow(right_wrong_grid, cmap= cmap)
    ax3.set_title('Right Wrong')
    ax3.axis('off')

    cmap = ListedColormap(["lawngreen", "blue", "grey", "red", "lawngreen", "red", "grey", "grey", "lawngreen"])
    confusion = array_compare(truths, predictions)
    confusion_grid = np.reshape(confusion, (int(np.sqrt(truths.shape[0])), -1))
    ax4.imshow(confusion_grid, cmap= cmap)
    ax4.set_title('Green: correct, B: false pos,\n R: false neg, Grey: Other')
    ax4.axis('off')

    confusion_matrix = count_occurrences(confusion).astype(int)
    ax5.axis('tight')
    ax5.axis('off')
    ax5.table(cellText=confusion_matrix,
              colLabels=['TrHealthy', 'TrRust', 'TrOther'],
              rowLabels=['PrHealthy', 'PrRust', 'PrOther'],
              cellLoc='center', loc='center')
    
    proc_user = proc_user_rates(confusion_matrix).astype(int)
    ax6.axis('tight')
    ax6.axis('off')
    ax6.table(cellText=proc_user,
              colLabels=['Healthy', 'Rust', 'Other'],
              rowLabels=['User %', 'Prod %'],
              cellLoc='center', loc='center')

    plt.tight_layout()
    plt.show()

def predict_class(model, data):
  predictions = model.predict(data)
  return np.argmax(predictions, axis=1)

## True utility
def convert_truths_to_integer(truths_array):
    num_samples = truths_array.shape[0]
    integer_truths = np.zeros(num_samples)
    for i in range(num_samples):
        integer_truths[i] = np.argmax(truths_array[i])
    return integer_truths

#elementwise and
def array_and(array1, array2):
    result = []
    for i in range(len(array1)):
        if array1[i] == array2[i]:
            result.append(1)
        else:
            result.append(0)
    return result

#compares arrays and seperates different states into ints
def array_compare(array1, array2):
    result = []
    for i in range(len(array1)):
        #(was healthy, predicted healthy)
        if array1[i] == 0 and array2[i] == 0:
            result.append(0)
        #(was healthy, predicted unhealthy)
        elif array1[i] == 0 and array2[i] == 1:
            result.append(1) 
        #(was healthy, predicted other)
        elif array1[i] == 0 and array2[i] == 2:
            result.append(2) 
        
        #(was unhealthy, predicted healthy)
        elif array1[i] == 1 and array2[i] == 0:
            result.append(3) 
        #(was unhealthy, predicted unhealthy)
        elif array1[i] == 1 and array2[i] == 1:
            result.append(4) 
        #(was unhealthy, predicted other)
        elif array1[i] == 1 and array2[i] == 2:
            result.append(5) 

        #(was other, predicted healthy)
        elif array1[i] == 2 and array2[i] == 0:
            result.append(6) 
        #(was other, predicted unhealthy)
        elif array1[i] == 2 and array2[i] == 1:
            result.append(7) 
        #(was other, predicted other)
        elif array1[i] == 2 and array2[i] == 2:
            result.append(8) 
        
        else:
            result.append(9)
    return result

def count_occurrences(arr):
    count = np.zeros((3,3))
    for i in range(len(arr)):
        if arr[i] == 0:
            count[0,0] += 1
        elif arr[i] == 1:
            count[0,1] += 1
        elif arr[i] == 2:
            count[0,2] += 1
        elif arr[i] == 3:
            count[1,0] += 1
        elif arr[i] == 4:
            count[1,1] += 1
        elif arr[i] == 5:
            count[1,2] += 1
        elif arr[i] == 6:
            count[2,0] += 1
        elif arr[i] == 7:
            count[2,1] += 1
        elif arr[i] == 8:
            count[2,2] += 1
    return np.transpose(count)

def proc_user_rates(confusion_matrix):
    output = np.zeros((2,3))

    output[0,0] = confusion_matrix[0,0] / (confusion_matrix[0,0] + confusion_matrix[0, 1] + confusion_matrix[0, 2])
    output[0,1] = confusion_matrix[1,1] / (confusion_matrix[1,0] + confusion_matrix[1, 1] + confusion_matrix[1, 2])
    output[0,2] = confusion_matrix[2,2] / (confusion_matrix[2,0] + confusion_matrix[2, 1] + confusion_matrix[2, 2])

    output[1,0] = confusion_matrix[0,0] / (confusion_matrix[0,0] + confusion_matrix[1, 0] + confusion_matrix[2, 0])
    output[1,1] = confusion_matrix[1,1] / (confusion_matrix[0,1] + confusion_matrix[1, 1] + confusion_matrix[2, 1])
    output[1,2] = confusion_matrix[2,2] / (confusion_matrix[0,2] + confusion_matrix[1, 2] + confusion_matrix[2, 2])

    output *= 100
    output = output.astype(int)
    return output